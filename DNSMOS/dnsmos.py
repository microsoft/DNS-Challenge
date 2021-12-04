import argparse
import glob
import json
import os

import numpy as np
import pandas as pd
import requests
import soundfile as sf
import librosa

from urllib.parse import urlparse, urljoin

# URL for the web service
SCORING_URI_DNSMOS = 'https://dnsmos.azurewebsites.net/score'
SCORING_URI_DNSMOS_P835 = 'https://dnsmos.azurewebsites.net/v1/dnsmosp835/score'
# If the service is authenticated, set the key or token
AUTH_KEY = '<Insert the key we provide in email here>'


# Set the content type
headers = {'Content-Type': 'application/json'}
# If authentication is enabled, set the authorization header
headers['Authorization'] = f'Basic {AUTH_KEY }'
def main(args):
    audio_clips_list = glob.glob(os.path.join(args.testset_dir, "*.wav"))
    scores = []
    for fpath in audio_clips_list:
        audio, fs = sf.read(fpath)
        if fs != 16000:
            print('Only sampling rate of 16000 is supported as of now')
            audio = librosa.core.resample(audio, fs, 16000)
        data = {"data": audio.tolist(), "filename": os.path.basename(fpath)}
        input_data = json.dumps(data)
        # Make the request and display the response
        if args.method == 'p808':
            u = SCORING_URI_DNSMOS
        else:
            u = SCORING_URI_DNSMOS_P835
        resp = requests.post(u, data=input_data, headers=headers)
        score_dict = resp.json()
        score_dict['file_name'] = os.path.basename(fpath)
        scores.append(score_dict)

    df = pd.DataFrame(scores)
    if args.method == 'p808':
        print('Mean MOS Score for the files is ', np.mean(df['mos']))
    else:
        print('Mean scores for the files: SIG[{}], BAK[{}], OVR[{}]'.format(np.mean(df['mos_sig']),np.mean(df['mos_bak']),np.mean(df['mos_ovr'])))

    if args.score_file:
        df.to_csv(args.score_file)



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testset_dir", required=True, 
                        help='Path to the dir containing audio clips to be evaluated')
    parser.add_argument('--score_file', help='If you want the scores in a CSV file provide the full path')
    parser.add_argument('--method', default='p808', const='p808', nargs='?', choices=['p808', 'p835'],
                        help='Choose which method to compute P.808 or P.835. Default is P.808')
    args = parser.parse_args()
    main(args)

