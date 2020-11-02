import argparse
import glob
import json
import os
import requests
import soundfile as sf


# URL for the web service
SCORING_URI = '<Insert the url we provide in email here>'
# If the service is authenticated, set the key or token
AUTH_KEY = '<Insert the key we provide in email here>'


# Set the content type
headers = {'Content-Type': 'application/json'}
# If authentication is enabled, set the authorization header
headers['Authorization'] = f'Bearer {AUTH_KEY }'
def main(args):
    audio_clips_list = glob.glob(os.path.join(args.testset_dir, "*.wav"))
    for fpath in audio_clips_list:
        audio, fs = sf.read(fpath)
        if fs != 16000:
            print('Only sampling rate of 16000 is supported as of now')
        data = {"data": audio.tolist()}
        input_data = json.dumps(data)
        # Make the request and display the response
        resp = requests.post(SCORING_URI, data=input_data, headers=headers)
        print(resp.json())



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testset_dir", required=True, 
                        help='Path to the dir containing audio clips to be evaluated')
    args = parser.parse_args()
    main(args)