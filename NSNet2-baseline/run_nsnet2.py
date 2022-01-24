#!/usr/bin/env python3
import argparse
import numpy as np
import soundfile as sf
from pathlib import Path
from enhance_onnx import NSnet2Enhancer

"""
    Inference script for NSnet2 baseline.
"""

def main(args):
    # check input path
    inPath = Path(args.input).resolve()
    assert inPath.exists()

    cfg = {
            'winlen'   : 0.02,
            'hopfrac'  : 0.5,
            'fs'       : args.fs,
            'mingain'  : -80,
            'feattype' : 'LogPow',
            'nfft'     : 320
        }

    if args.fs == 48000:
        cfg['nfft'] = 1024

    # Create the enhancer
    enhancer = NSnet2Enhancer(modelfile=args.model, cfg=cfg)

    # get modelname
    modelname = Path(args.model).stem

    if inPath.is_file() and inPath.suffix == '.wav':
        # input is single .wav file
        sigIn, fs = sf.read(str(inPath))
        if len(sigIn.shape) > 1:
            sigIn = sigIn[:,0]

        outSig = enhancer(sigIn, fs)

        outname = './{:s}_{:s}.wav'.format(inPath.stem, modelname)
        if args.output:
            # write in given dir
            outdir = Path(args.output)
            outdir.mkdir(exist_ok=True)
            outpath = outdir.joinpath(outname)
        else:
            # write in current work dir
            outpath = Path(outname)

        print('Writing output to:', str(outpath))
        sf.write(outpath.resolve(), outSig, fs)

    elif inPath.is_dir():
        # input is directory
        if args.output:
            # full provided path
            outdir = Path(args.output).resolve()
        else:
            outdir = inPath.parent.joinpath(modelname).resolve()

        outdir.mkdir(parents=True, exist_ok=True)
        print('Writing output to:', str(outdir))

        fpaths = list(inPath.glob('*.wav'))

        for ii, path in enumerate(fpaths):
            print(f"Processing file [{ii+1}/{len(fpaths)}]")
            print(path)

            sigIn, fs = sf.read(str(path))

            if len(sigIn.shape) > 1:
                sigIn = sigIn[:,0]

            outSig = enhancer(sigIn, fs)
            outpath = outdir / path.name
            outpath = str(outpath)
            sf.write(outpath, outSig, fs)

    else:
        raise ValueError("Invalid input path.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--model", type=str, help="Path to ONNX model.", default='nsnet2-20ms-48k-baseline.onnx')
    parser.add_argument("-i", "--input", type=str, help="Path to noisy speech wav file or directory.")
    parser.add_argument("-o", "--output", type=str, help="Optional output directory.", required=False)
    parser.add_argument("-fs", type=int, help="Sampling rate of the input audio", default=48000)
    args = parser.parse_args()

    main(args)
