import argparse
import numpy as np
import soundfile as sf
from pathlib import Path
import onnxruntime as ort

import featurelib
import torch
import scipy
import scipy.signal

class NSnet2Enhancer(object):
    """NSnet2 enhancer class."""

    def __init__(self, modelfile, cfg=None):
        """Instantiate NSnet2 given a trained model path."""
        self.cfg = cfg
        self.frameShift = float(self.cfg['winlen'])* float(self.cfg["hopfrac"])
        self.fs = int(self.cfg['fs'])
        self.mingain = 10**(self.cfg['mingain']/20)
        self.N_win = int(float(self.cfg['winlen']) * self.fs)
        if 'nfft' in cfg:
            self.N_fft = int(self.cfg['nfft'])
        else:
            self.N_fft = self.N_win
        self.N_hop = int(self.N_fft * float(cfg["hopfrac"]))
        
        """load onnx model"""
        self.ort = ort.InferenceSession(modelfile)
        self.dtype = np.float32
        self.win = np.sqrt(scipy.signal.windows.hann(self.N_win, sym=False))
        self.win_buf = torch.from_numpy(self.win).float()        
        L = len(self.win)
        awin = np.zeros_like(self.win)
        for k in range(0, self.N_hop):
            idx = range(k, L, self.N_hop)
            H = self.win[idx]
            awin[idx] = np.linalg.pinv(H[:,np.newaxis])
        self.awin = torch.from_numpy(awin).float()

    def enhance(self, x):
        """Obtain the estimated filter"""
        onnx_inputs = {self.ort.get_inputs()[0].name: x.astype(self.dtype)}
        out = self.ort.run(None, onnx_inputs)[0][0]
        return out

    def enhance_48khz(self, x):
        """Run model on single sequence"""
        if len(x.shape) < 2:
            x = torch.from_numpy(np.expand_dims(x, 0)).float()
        else:
            x = x.transpose()
        # x: [channels, samples]

        sig_framed = torch.nn.functional.conv1d(x.unsqueeze(1), weight=torch.diag(self.win_buf).unsqueeze(1), stride=self.N_hop).permute(0,2,1).contiguous()
        spec = torch.fft.rfft(sig_framed, n=self.N_fft)
        spec = torch.stack((spec.real, spec.imag), dim=-1)
        feat = torch.log10(torch.sum(spec**2, dim=-1).clamp_min(1e-12))
        onnx_inputs = {self.ort.get_inputs()[0].name: feat.numpy().astype(self.dtype)}
        out = self.ort.run(None, onnx_inputs)[0]
        out = torch.from_numpy(out).float()
        out_spec = out.unsqueeze(3) * spec
        out_spec_restacked = torch.complex(out_spec[:,:,:,0], out_spec[:,:,:,1]).contiguous()
        x_framed = torch.fft.irfft(out_spec_restacked, n=self.N_fft)[:,:,0:self.N_win]
        # overlapp-add using conv_transpose
        sig = torch.nn.functional.conv_transpose1d(x_framed.permute(0,2,1), weight=torch.diag(self.awin).unsqueeze(1), stride=self.N_hop).squeeze(1).contiguous()
        return sig[0]

    def __call__(self, sigIn, inFs):
        """Enhance a single Audio signal."""
        assert inFs in (16000, 48000), "Inconsistent sampling rate!"

        if inFs == 48000:
            return self.enhance_48khz(sigIn)

        inputSpec = featurelib.calcSpec(sigIn, self.cfg)
        inputFeature = featurelib.calcFeat(inputSpec, self.cfg)
        # shape: [batch x time x freq]
        inputFeature = np.expand_dims(np.transpose(inputFeature), axis=0)

        # Obtain network output
        out = self.enhance(inputFeature)
        
        # limit suppression gain
        Gain = np.transpose(out)
        Gain = np.clip(Gain, a_min=self.mingain, a_max=1.0)
        outSpec = inputSpec * Gain

        # go back to time domain
        sigOut = featurelib.spec2sig(outSpec, self.cfg)

        return sigOut
