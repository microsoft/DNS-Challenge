#!/usr/bin/env python3
"""
Runnable script to invoke
noise_suppression.nsnet.inference.onnx
"""

import os
import glob
import logging
import pathlib
import concurrent.futures
import argparse
import onnx as ns_onnx

# pylint: disable=too-few-public-methods
class Worker:
    """
    Delayed constructor of NSNetInference to make sure each
    multiprocessing worker has its own instance of the ONNX model.
    """
    nsnet = None

    def __init__(self, *args):
        self.args = args

    def __call__(self, fname):
        if Worker.nsnet is None:
            # pylint: disable=no-value-for-parameter
            Worker.nsnet = ns_onnx.NSNetInference(*self.args)
        logging.debug("NSNet/ONNX: process file %s", fname)
        Worker.nsnet(fname)


def _main():

    parser = argparse.ArgumentParser(description='NSNet Noise Suppressor inference', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--noisyspeechdir', required=True, help="Input directory with noisy WAV files")
    parser.add_argument('--enhanceddir', required=True, help="Output directory to save enhanced WAV files")
    parser.add_argument('--modelpath', required=True, help="ONNX model to use for inference")
    parser.add_argument('--window_length', type=float, default=0.02)
    parser.add_argument('--hopfraction', type=float, default=0.5)
    parser.add_argument('--dft_size', type=int, default=512)
    parser.add_argument('--sampling_rate', type=int, default=16000)
    parser.add_argument('--spectral_floor', type=float, default=-120.0)
    parser.add_argument('--timesignal_floor', type=float, default=1e-12)
    parser.add_argument('--audioformat', default="*.wav")
    parser.add_argument('--num_workers', type=int, default=4,
               help="Number of OS processes to run in parallel")
    parser.add_argument('--chunksize', type=int, default=1,
               help="Number of files per worker to process in one batch")

    args = parser.parse_args()

    logging.info("NSNet inference args: %s", args)

    input_filelist = glob.glob(os.path.join(args.noisyspeechdir, args.audioformat))
    pathlib.Path(args.enhanceddir).mkdir(parents=True, exist_ok=True)

    worker = Worker(args.modelpath, args.window_length, args.hopfraction,
                    args.dft_size, args.sampling_rate, args.enhanceddir)

    logging.debug("NSNet local workers start with %d input files", len(input_filelist))

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.num_workers) as executor:
        executor.map(worker, input_filelist, chunksize=args.chunksize)
#    for fname in input_filelist:
#        worker(fname)
        
    logging.info("NSNet local workers complete")


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.DEBUG)  # Use logging.WARNING in prod

if __name__ == '__main__':
    _main()
