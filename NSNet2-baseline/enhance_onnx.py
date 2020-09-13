import argparse
import numpy as np
import soundfile as sf
from pathlib import Path
import onnxruntime as ort

import featurelib


class NSnet2Enhancer(object):
    """NSnet2 enhancer class."""

    def __init__(self, modelfile, cfg=None):
        """Instantiate NSnet2 given a trained model path."""
        self.cfg = {
            'winlen'   : 0.02,
            'hopfrac'  : 0.5,
            'fs'       : 16000,
            'mingain'  : -80,
            'feattype' : 'LogPow'
        }
        self.frameShift = float(self.cfg['winlen'])* float(self.cfg["hopfrac"])
        self.fs = int(self.cfg['fs'])
        self.Nfft = int(float(self.cfg['winlen'])*self.fs)
        self.mingain = 10**(self.cfg['mingain']/20)
        
        """load onnx model"""
        self.ort = ort.InferenceSession(modelfile)
        self.dtype = np.float32

    def enhance(self, x):
        """Obtain the estimated filter"""
        onnx_inputs = {self.ort.get_inputs()[0].name: x.astype(self.dtype)}
        out = self.ort.run(None, onnx_inputs)[0][0]
        return out

    def __call__(self, sigIn, inFs):
        """Enhance a single Audio signal."""
        assert inFs == self.fs, "Inconsistent sampling rate!"

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
