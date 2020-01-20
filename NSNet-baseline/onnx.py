"""
Run NSNet inference using onnxruntime.
"""

import os
import math
import logging

import numpy as np
import soundfile as sf
import onnxruntime

import audiolib


# pylint: disable=too-few-public-methods
class NSNetInference:
    "Apply NSNet ONNX model to WAV files"

    def __init__(self, model_path, window_length, hop_fraction,
                 dft_size, sampling_rate, output_dir=None,
                 spectral_floor=-120.0, timesignal_floor=1e-12):
        self.hop_fraction = hop_fraction
        self.dft_size = dft_size
        self.sampling_rate = sampling_rate
        self.output_dir = output_dir
        self.spectral_floor = spectral_floor
        self.timesignal_floor = timesignal_floor
        self.framesize = int(window_length * sampling_rate)
        self.wind = audiolib.hamming(self.framesize, hop=hop_fraction)
        self.model = onnxruntime.InferenceSession(model_path)

    # pylint: disable=too-many-locals,invalid-name
    def __call__(self, noisy_speech_filename, output_dir=None):
        "Apply NSNet model to one file and produce an output file with clean speech."

        enhanced_filename = os.path.join(output_dir or self.output_dir,
                                         os.path.basename(noisy_speech_filename))

        logging.info("NSNet inference: %s", noisy_speech_filename)
        sig, sample_rate = sf.read(noisy_speech_filename)

        ssize = len(sig)
        print('ssize:', ssize)
        fsize = len(self.wind)
        hsize = int(self.hop_fraction * self.framesize)

        sstart = hsize - fsize
        print('sstart:', sstart)
        send = ssize
        nframe = math.ceil((send - sstart) / hsize)
        zpleft = -sstart
        zpright = (nframe - 1) * hsize + fsize - zpleft - ssize

        if zpleft > 0 or zpright > 0:
            sigpad = np.zeros(ssize + zpleft + zpright)
            sigpad[zpleft:len(sigpad)-zpright] = sig
        else:
            sigpad = sig

        sout = np.zeros(nframe * hsize)
        x_old = np.zeros(hsize)

        model_input_names = [inp.name for inp in self.model.get_inputs()]
        model_inputs = {
            inp.name: np.zeros(
                [dim if isinstance(dim, int) else 1 for dim in inp.shape],
                dtype=np.float32)
            for inp in self.model.get_inputs()[1:]}

        mu = None
        sigmasquare = None
        frame_count = 0

        for frame_sampleindex in range(0, nframe * hsize, hsize):

            # second frame starts from mid-of first frame and goes until frame-size
            sigpadframe = sigpad[frame_sampleindex:frame_sampleindex + fsize] * self.wind

            xmag, xphs = audiolib.magphasor(audiolib.stft(
                sigpadframe, self.sampling_rate, self.wind,
                self.hop_fraction, self.dft_size, synth=True, zphase=False))

            feat = audiolib.logpow(xmag, floor=self.spectral_floor)

            if frame_sampleindex == 0:
                mu = feat
                sigmasquare = feat**2

            norm_feat, mu, sigmasquare, frame_count = audiolib.onlineMVN_perframe(
                feat, frame_counter=frame_count, mu=mu, sigmasquare=sigmasquare,
                frameshift=0.01, tauFeat=3., tauFeatInit=0.1, t_init=0.1)

            norm_feat = norm_feat[np.newaxis, np.newaxis, :]

            model_inputs['input'] = np.float32(norm_feat)
            model_outputs = self.model.run(None, model_inputs)
            model_inputs = dict(zip(model_input_names, model_outputs))

            mask = model_outputs[0].squeeze()
            x_enh = audiolib.istft(
                (xmag * mask) * xphs, sample_rate, self.wind, self.dft_size, zphase=False)

            sout[frame_sampleindex:frame_sampleindex + hsize] = x_old + x_enh[0:hsize]
            x_old = x_enh[hsize:fsize]

        xfinal = sout
        audiolib.audiowrite(xfinal, sample_rate, enhanced_filename, norm=False)
