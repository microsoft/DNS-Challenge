# -*- coding: utf-8 -*-
"""
Functions for audio featurization.
"""

import os
import math
import logging

import numpy as np
import soundfile as sf
import librosa

SIGMA_EPS = 1e-12


def stft(frame, _sr, wind, _hop, nfft, synth=False, zphase=False):
    if not zphase:
        return np.fft.rfft(frame, n=nfft)
    fsize = len(wind)
    woff = (fsize - (fsize % 2)) // 2
    zp = np.zeros(nfft - fsize)
    return np.fft.rfft(np.concatenate((frame[woff:], zp, frame[:woff])))


def istft(frame, _sr, wind, nfft, zphase=False):
    frame = np.fft.irfft(frame, nfft)
    if zphase:
        fsize = len(wind)
        frame = np.roll(frame, (fsize - (fsize % 2)) // 2)[:fsize]
    return frame


def onlineMVN_perframe(
        frame_feature, frame_counter, mu, sigmasquare,
        frameshift=0.01, tauFeat=3., tauFeatInit=0.1, t_init=0.1):
    """Online mean and variance normalization (per frequency)"""

    n_init_frames = math.ceil(t_init / frameshift)
    alpha_feat_init = math.exp(-frameshift / tauFeatInit)
    alpha_feat = math.exp(-frameshift / tauFeat)

    if frame_counter < n_init_frames:
        alpha = alpha_feat_init
    else:
        alpha = alpha_feat

    mu = alpha * mu + (1 - alpha) * frame_feature
    sigmasquare = alpha * sigmasquare + (1 - alpha) * frame_feature**2
    sigma = np.sqrt(np.maximum(sigmasquare - mu**2, SIGMA_EPS)) # limit for sqrt
    norm_feature = (frame_feature - mu) / sigma
    frame_counter += 1

    return norm_feature, mu, sigmasquare, frame_counter


def magphasor(complexspec):
    """Decompose a complex spectrogram into magnitude and unit phasor.
    m, p = magphasor(c) such that c == m * p.
    """
    mspec = np.abs(complexspec)
    pspec = np.empty_like(complexspec)
    zero_mag = mspec == 0.  # fix zero-magnitude
    pspec[zero_mag] = 1.
    pspec[~zero_mag] = complexspec[~zero_mag] / mspec[~zero_mag]
    return mspec, pspec


def logpow(sig, floor=-30.):
    """Compute log power of complex spectrum.

    Floor any -`np.inf` value to (nonzero minimum + `floor`) dB.
    If all values are 0s, floor all values to -80 dB.
    """
    log10e = np.log10(np.e)
    pspec = sig.real**2 + sig.imag**2
    zeros = pspec == 0
    logp = np.empty_like(pspec)
    if np.any(~zeros):
        logp[~zeros] = np.log(pspec[~zeros])
        logp[zeros] = np.log(pspec[~zeros].min()) + floor / 10 / log10e
    else:
        logp.fill(-80 / 10 / log10e)

    return logp


def hamming(wsize, hop=None):
    "Compute the Hamming window"

    if hop is None:
        return np.hamming(wsize)

    # For perfect OLA reconstruction in time
    if wsize % 2:  # Fix endpoint problem for odd-size window
        wind = np.hamming(wsize)
        wind[0] /= 2.
        wind[-1] /= 2.
    else:  # even-size window
        wind = np.hamming(wsize + 1)
        wind = wind[:-1]

    assert tnorm(wind, hop), \
        "[wsize:{}, hop:{}] violates COLA in time.".format(wsize, hop)

    return wind


def tnorm(wind, hop):
    amp = tcola(wind, hop)
    if amp is None:
        return False
    wind /= amp
    return True


def tcola(wind, _hop):
    wsize = len(wind)
    hsize = 160
    buff = wind.copy()  # holds OLA buffer and account for time=0
    for wi in range(hsize, wsize, hsize):  # window moving forward
        wj = wi + wsize
        buff[wi:] += wind[:wsize - wi]
    for wj in range(wsize - hsize, 0, -hsize):  # window moving backward
        wi = wj - wsize
        buff[:wj] += wind[wsize - wj:]

    if np.allclose(buff, buff[0]):
        return buff[0]

    return None


def audioread(path, sr=None, start=0, stop=None, mono=True, norm=False):

    path = os.path.abspath(path)
    if not os.path.exists(path):
        logging.error('File does not exist: %s', path)
        raise ValueError("[{}] does not exist!".format(path))

    try:
        x, xsr = sf.read(path, start=start, stop=stop)
    except RuntimeError:  # fix for sph pcm-embedded shortened v2
        logging.warning('Audio type not supported for file %s. Trying sph2pipe...', path)

    if len(x.shape) == 1:  # mono
        if sr and xsr != sr:
            print("Resampling to sampling rate:", sr)
            x = librosa.resample(x, xsr, sr)
            xsr = sr
        if norm:
            print("Normalization input data")
            x /= np.max(np.abs(x))
        return x, xsr

    # multi-channel
    x = x.T
    if sr and xsr != sr:
        x = librosa.resample(x, xsr, sr, axis=1)
        xsr = sr
    if mono:
        x = x.sum(axis=0) / x.shape[0]
    if norm:
        for chan in range(x.shape[0]):
            x[chan, :] /= np.max(np.abs(x[chan, :]))

    return x, xsr


def audiowrite(data, sr, outpath, norm=False):

    logging.debug("Writing to: %s", outpath)

    if np.max(np.abs(data)) == 0: # in case all entries are 0s
        logging.warning("All-zero output! Something is not quite right,"
                        " check your input audio clip and model.")

    outpath = os.path.abspath(outpath)
    outdir = os.path.dirname(outpath)

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    sf.write(outpath, data, sr)
