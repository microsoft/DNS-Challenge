# Usage:
# python dnsmos_local.py -ms sig.onnx -mbo bak_ovr.onnx 
#                           -t .


import glob
import os
import csv
import numpy as np
import math
import argparse
import soundfile as sf
import random
import librosa
import onnxruntime as ort
import numpy.polynomial.polynomial as poly
from tqdm import tqdm

# Coefficients for polynomial fitting
COEFS_SIG = np.array([9.651228012789436761e-01, 6.592637550310214145e-01, 
                    7.572372955623894730e-02])
COEFS_BAK = np.array([-3.733460011101781717e+00,2.700114234092929166e+00,
                    -1.721332907340922813e-01])
COEFS_OVR = np.array([8.924546794696789354e-01, 6.609981731940616223e-01,
                    7.600269530243179694e-02])

def main(args):

    def audio_logpowspec(audio, nfft=320, hop_length=160, sr=16000):
        powspec = (np.abs(librosa.core.stft(audio, n_fft=nfft, hop_length=hop_length)))**2
        logpowspec = np.log10(np.maximum(powspec, 10**(-12)))
        return logpowspec.T

    predicted_mos_sig = []
    predicted_mos_bak = []
    predicted_mos_ovr = []
    audio_clips_list = glob.glob(os.path.join(args.testset_dir, "*.wav"))

    session_sig = ort.InferenceSession(args.sig_model_path)
    session_bak_ovr = ort.InferenceSession(args.bak_ovr_model_path)

    if args.csv_path:
        csv_path = args.csv_path
    else:
        csv_path = args.run_name+'.csv'

    with open(csv_path, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['filename', 'SIG', 'BAK', 'OVR'])

        for i in tqdm(range(len(audio_clips_list))):
            fpath = audio_clips_list[i]
            audio, fs = sf.read(fpath)
            if len(audio)<2*fs:
                print('Audio clip is too short. Skipped processing ', 
                        os.path.basename(fpath))
                continue
            len_samples = int(args.input_length*fs)
            while len(audio) < len_samples:
                audio = np.append(audio, audio)
            
            num_hops = int(np.floor(len(audio)/fs) - args.input_length)+1
            hop_len_samples = fs
            predicted_mos_sig_seg = []
            predicted_mos_bak_seg = []
            predicted_mos_ovr_seg = []

            for idx in range(num_hops):
                audio_seg = audio[int(idx*hop_len_samples) : int((idx+args.input_length)*hop_len_samples)]
                input_features = np.array(audio_logpowspec(audio=audio_seg, sr=fs)).astype('float32')[np.newaxis,:,:]

                onnx_inputs_sig = {inp.name: input_features for inp in session_sig.get_inputs()}
                mos_sig = poly.polyval(session_sig.run(None, onnx_inputs_sig), COEFS_SIG)
                    
                onnx_inputs_bak_ovr = {inp.name: input_features for inp in session_bak_ovr.get_inputs()}
                mos_bak_ovr = session_bak_ovr.run(None, onnx_inputs_bak_ovr)

                mos_bak = poly.polyval(mos_bak_ovr[0][0][1], COEFS_BAK)
                mos_ovr = poly.polyval(mos_bak_ovr[0][0][2], COEFS_OVR)

                
                predicted_mos_sig_seg.append(mos_sig)
                predicted_mos_bak_seg.append(mos_bak)
                predicted_mos_ovr_seg.append(mos_ovr)

            predicted_mos_sig.append(np.mean(predicted_mos_sig_seg))
            predicted_mos_bak.append(np.mean(predicted_mos_bak_seg))
            predicted_mos_ovr.append(np.mean(predicted_mos_ovr_seg))

            csvwriter.writerow([os.path.basename(fpath), np.mean(predicted_mos_sig_seg),
                            np.mean(predicted_mos_bak_seg), np.mean(predicted_mos_ovr_seg)])

        print("The average SIG, BAK and OVR MOS for {0} is {1}, {2}, {3}".format(args.run_name, 
                                        str(round(np.mean(predicted_mos_sig), 2)), 
                                        str(round(np.mean(predicted_mos_bak), 2)),
                                        str(round(np.mean(predicted_mos_ovr), 2))))

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-ms', "--sig_model_path", default='sig.onnx', 
                        help='Path to ONNX or ckpt model for SIG prediction')
    parser.add_argument('-mbo', "--bak_ovr_model_path", default='bak_ovr.onnx', 
                        help='Path to ONNX or ckpt model for BAK and OVR prediction')
    parser.add_argument('-t', "--testset_dir", default='.', 
                        help='Path to the dir containing audio clips in .wav to be evaluated')
    parser.add_argument('-o', "--csv_path", default=None, help='Dir to the csv that saves the results')
    parser.add_argument('-l', "--input_length", type=int, default=9)
    parser.add_argument('-r', "--run_name", type=str, default="dnsmos_p835_inference_sig_bak_ovr_test", 
                        help='Change the name depending on the test set and DNS model being evaluated')
    
    args = parser.parse_args()

    main(args)
