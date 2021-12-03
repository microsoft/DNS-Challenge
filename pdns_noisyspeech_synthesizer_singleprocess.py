"""
@author: hadubey
"""

# Note: This single process audio synthesizer will attempt to use each clean
# speech sourcefile once, as it does not randomly sample from these files

import os
import glob
import argparse
import ast
import configparser as CP
from random import shuffle
import random

import librosa
import numpy as np
from scipy import signal

import sys
sys.path.insert(0,'/mnt/f/4th_DNSChallenge/ICASSP_2022/DNS-Challenge')
from audiolib import audioread, audiowrite, segmental_snr_mixer, activitydetector, is_clipped, add_clipping
import utils

import pandas as pd
from pathlib import Path
from scipy.io import wavfile

import csv
import random
random.seed(5)

MAXTRIES = 50
MAXFILELEN = 100

np.random.seed(5)
random.seed(5)

def add_pyreverb(clean_speech, rir):
    #
    #print(len(clean_speech))
    #print(len(rir))
    reverb_speech = signal.fftconvolve(clean_speech, rir, mode="full")
    
    # make reverb_speech same length as clean_speech
    reverb_speech = reverb_speech[0 : clean_speech.shape[0]]

    return reverb_speech

def build_audio3(is_clean, params, spk_index, audio_samples_length=-1):
    '''Construct an audio signal from source files of primary speaker
    Returns a list of all segments belonging to primary speaker'''

    fs_output = params['fs']
    silence_length = params['silence_length']

    if audio_samples_length == -1:
        audio_samples_length = int(params['audio_length']*params['fs'])

    output_audio = np.zeros(0)
    remaining_length = audio_samples_length
    files_used = []
    clipped_files = []

    if is_clean:
        source_files = params['cleanfilenames']
        idx = spk_index

    input_audio, fs_input = audioread(source_files[idx])
        
    if fs_input != fs_output:
        input_audio = librosa.resample(input_audio, fs_input, fs_output)

    num_segs= int(input_audio.shape[0]/(params['fs']*params['audio_length']))
    # if current file is longer than remaining desired length, and this is
    # noise generation or this is training set, subsample it randomly

    remaining_length = input_audio.shape[0]
    start_idx= 0 

    audios_all = []

    for seg in range(0,num_segs):
        # print(seg)

        audio_temp = input_audio[seg*audio_samples_length : (seg + 1)*audio_samples_length]

        if not is_clipped(audio_temp):
            audios_all.append(audio_temp)
            files_used.append(source_files[idx])
        else:
            clipped_files.append(source_files[idx])
        
    return audios_all, files_used, clipped_files
    # output_audio, files_used, clipped_files, idx

# idx = np.random.randint(0, np.size(source_files))
# # initialize silence
# silence = np.zeros(int(fs_output*silence_length))

    # iterate through multiple clips until we have a long enough signal
    # tries_left = MAXTRIES
    # while remaining_length > 0 and tries_left > 0:

        # read next audio file and resample if necessary
        # idx = (idx + 1) % np.size(source_files)

        # source_files= 

def build_audio(is_clean, params, index, audio_samples_length=-1):
    '''Construct an audio signal from source files'''

    fs_output = params['fs']
    silence_length = params['silence_length']

    if audio_samples_length == -1:
        audio_samples_length = int(params['audio_length']*params['fs'])

    output_audio = np.zeros(0)
    remaining_length = audio_samples_length
    files_used = []
    clipped_files = []

    if is_clean:
        source_files = params['cleanfilenames']
        idx = index
    else:
        if 'noisefilenames' in params.keys():
            source_files = params['noisefilenames']
            idx = index
        # if noise files are organized into individual subdirectories, pick a directory randomly
        else:
            noisedirs = params['noisedirs']
            # pick a noise category randomly
            idx_n_dir = np.random.randint(0, np.size(noisedirs))
            source_files = glob.glob(os.path.join(noisedirs[idx_n_dir], 
                                                  params['audioformat']))
            shuffle(source_files)
            # pick a noise source file index randomly
            idx = np.random.randint(0, np.size(source_files))

    # initialize silence
    silence = np.zeros(int(fs_output*silence_length))

    # iterate through multiple clips until we have a long enough signal
    tries_left = MAXTRIES

    while remaining_length > 0 and tries_left > 0:

        # read next audio file and resample if necessary
        idx = (idx + 1) % np.size(source_files)
        input_audio, fs_input = audioread(source_files[idx])
        if fs_input != fs_output:
            input_audio = librosa.resample(input_audio, fs_input, fs_output)

        # if current file is longer than remaining desired length, and this is
        # noise generation or this is training set, subsample it randomly
        if len(input_audio) > remaining_length and (not is_clean or params['is_test_set']):
#         if len(input_audio) > remaining_length and (not is_clean or not params['is_test_set']):

            idx_seg = np.random.randint(0, len(input_audio)-remaining_length)
            input_audio = input_audio[idx_seg:idx_seg+remaining_length]

        # check for clipping, and if found move onto next file
        if is_clipped(input_audio):
            clipped_files.append(source_files[idx])
            tries_left -= 1
            continue

        # concatenate current input audio to output audio stream
        files_used.append(source_files[idx])
        output_audio = np.append(output_audio, input_audio)
        remaining_length -= len(input_audio)

        # add some silence if we have not reached desired audio length
        if remaining_length > 0:
            silence_len = min(remaining_length, len(silence))
            output_audio = np.append(output_audio, silence[:silence_len])
            remaining_length -= silence_len

    if tries_left == 0 and not is_clean and 'noisedirs' in params.keys():
        print("There are not enough non-clipped files in the " + noisedirs[idx_n_dir] + \
              " directory to complete the audio build")
        return [], [], clipped_files, idx

    return output_audio, files_used, clipped_files, idx

def build_audio2(is_clean, params, index, audio_samples_length=-1):
    '''Construct an audio signal from source files'''

    fs_output = params['fs']
    silence_length = params['silence_length']
    
    if audio_samples_length == -1:
        audio_samples_length = int(params['audio_length']*params['fs'])

    output_audio = np.zeros(0)
    remaining_length = audio_samples_length
    files_used = []
    clipped_files = []

    if is_clean:
        source_files = params['cleanfilenames2']
        idx = index

    # initialize silence
    silence = np.zeros(int(fs_output*silence_length))

    # iterate through multiple clips until we have a long enough signal
    tries_left = MAXTRIES

    while remaining_length > 0 and tries_left > 0:
        # read next audio file and resample if necessary
        idx = (idx + 1) % np.size(source_files)
        input_audio, fs_input = audioread(source_files[idx])

        if fs_input != fs_output:
            input_audio = librosa.resample(input_audio, fs_input, fs_output)

        # if current file is longer than remaining desired length, and this is
        # noise generation or this is training set, subsample it randomly
        if len(input_audio) > remaining_length:
#         if len(input_audio) > remaining_length and (not is_clean or not params['is_test_set']):
            idx_seg = np.random.randint(0, len(input_audio)-remaining_length)
            input_audio = input_audio[idx_seg:idx_seg+remaining_length]

        # check for clipping, and if found move onto next file
        if is_clipped(input_audio):
            clipped_files.append(source_files[idx])
            tries_left -= 1
            continue

        # concatenate current input audio to output audio stream
        files_used.append(source_files[idx])
        output_audio = np.append(output_audio, input_audio)
        remaining_length -= len(input_audio)

        # add some silence if we have not reached desired audio length
        if remaining_length > 0:
            silence_len = min(remaining_length, len(silence))
            output_audio = np.append(output_audio, silence[:silence_len])
            remaining_length -= silence_len

    if tries_left == 0:
        print("There are not enough non-clipped files in the " + noisedirs[idx_n_dir] + \
              " directory to complete the audio build")
        return [], [], clipped_files, idx

    return output_audio, files_used, clipped_files, idx

def gen_audio(is_clean, params, index, audio_samples_length=-1):
    '''Calls build_audio() to get an audio signal from noise set.
    Verify that it meets the activity threshold'''

    clipped_files = []
    low_activity_files = []

    if audio_samples_length == -1:
        audio_samples_length = int(params['audio_length']*params['fs'])
    
    if is_clean:
        activity_threshold = params['clean_activity_threshold']
    else:
        activity_threshold = params['noise_activity_threshold']

    while True:
        audio, source_files, new_clipped_files, index = \
            build_audio(is_clean, params, index, audio_samples_length)

        clipped_files += new_clipped_files
        if len(audio) < audio_samples_length:
            continue

        if activity_threshold == 0.0:
            break

        percactive = activitydetector(audio=audio)
        if percactive > activity_threshold:
            break
        else:
            low_activity_files += source_files

    return audio, source_files, clipped_files, low_activity_files, index

def gen_audio2(is_clean, params, index, audio_samples_length=-1):
    '''Calls build_audio3() to get an audio signal from secondary speaker. Secondary speaker
    is randomly chosen. Verify that it meets the
       activity threshold'''

    clipped_files = []
    low_activity_files = []

    if audio_samples_length == -1:
        audio_samples_length = int(params['audio_length']*params['fs'])
    
    if is_clean:
        activity_threshold = params['clean_activity_threshold']
    else:
        activity_threshold = params['noise_activity_threshold']

    while True:
        audio, source_files, new_clipped_files, index = \
            build_audio2(is_clean, params, index, audio_samples_length)

        clipped_files += new_clipped_files
        if len(audio) < audio_samples_length:
            continue

        if activity_threshold == 0.0:
            break

        percactive = activitydetector(audio=audio)
        if percactive > activity_threshold:
            break
        else:
            low_activity_files += source_files

    return audio, source_files, clipped_files, low_activity_files, index

def gen_audio3(is_clean, params, spk_index, audio_samples_length=-1):
    '''Calls build_audio() to get an Primary speaker audio signal [ensure one unique speaker, track
    spk ids], and verify that it meets the activity threshold'''

#    clipped_files = []
    low_activity_files = []

    if audio_samples_length == -1:
        audio_samples_length = int(params['audio_length']*params['fs'])
    
    if is_clean:
        activity_threshold = params['clean_activity_threshold']
    else:
        activity_threshold = params['noise_activity_threshold']

    #for spk_index in range(0,len(params['cleanfilenames'])):
    audios_all, files_used, clipped_files  = build_audio3(is_clean, params, spk_index)

    chosen_audio=[]

    for audio in audios_all:
        percactive = activitydetector(audio=audio)
        if activity_threshold == 0.0 or percactive > activity_threshold:
            chosen_audio.append(audio)

    return chosen_audio

def main_gen(params):
    '''Calls gen_audio() to generate the audio signals, verifies that they meet
       the requirements, and writes the files to storage'''

    clean_source_files = []
    clean_clipped_files = []
    clean_low_activity_files = []
    
    clean_source_files2 = []
    clean_clipped_files2 = []
    clean_low_activity_files2 = []
        
    noise_source_files = []
    noise_clipped_files = []
    noise_low_activity_files = []

    clean_index = 0
    clean_index2 = 0
    noise_index = 0

    file_num = params['fileindex_start']
    cleanfilenames= params['cleanfilenames'] 
    cleanfilenames2= params['cleanfilenames2'] 

    # spk_index = 0 # start of speaker index
    num_spk = len(cleanfilenames)

    while file_num <= params['fileindex_end']:
        # generate clean speech
        #clean, clean_sf, clean_cf, clean_laf, clean_index = \
        #    gen_audio(True, params, clean_index)
        spk_index = random.randint(0,len(params['cleanfilenames'])-1)   

        chosen_clean= gen_audio3(True, params, spk_index)
        num_clips= int(len(chosen_clean))

        #(True, params, clean_index) 
        # add reverb with selected RIR
        #rir_index = random.randint(0,len(params['myrir'])-1)
        
        num_to_select1 = 1
        rirfilenames = params['myrir']

        chosen_clean_reverb=[]

        for clean in chosen_clean:
            myrir= random.sample(rirfilenames, num_to_select1)
            (fs_rir,samples_rir) = wavfile.read(myrir[0])

            if len(samples_rir.shape) > 1:
                channel = random.randint(0,len(samples_rir.shape)-1)
                samples_rir_ch = samples_rir[:,channel]
            else:
                samples_rir_ch = samples_rir
            
            clean_reverb = add_pyreverb(clean, samples_rir_ch)
            chosen_clean_reverb.append(clean_reverb)

        # add secondary speech and/or noise for each chunck of primary speech
        for chose_primary in chosen_clean_reverb:
            index2 = random.randint(0,len(params['cleanfilenames2'])-1)  

            clean2, clean_sf, clean_cf, clean_laf, clean_index = \
                gen_audio2(True, params, index2, chose_primary.shape[0])
            
            noise_index = random.randint(0,len(params['noisefilenames'])-1)
            # generate noise
            noise, noise_sf, noise_cf, noise_laf, noise_index = \
                gen_audio(False, params, noise_index, chose_primary.shape[0])

            # if specified, use specified SNR value
            if not params['randomize_snr']:
                snr = params['snr']
            # use a randomly sampled SNR value between the specified bounds
            else:
                snr = np.random.randint(params['snr_lower'], params['snr_upper'])
                snr2 = np.random.randint(params['snr_lower'], params['snr_upper'])
                snr3 = np.random.randint(params['snr_lower'], params['snr_upper'])

            # 1. Primary(clean) + Noise
            clean_snr, noise_snr, noisy_snr, target_level = segmental_snr_mixer(params=params, 
                                                                    clean=chose_primary, 
                                                                    noise=noise, 
                                                                    snr=snr)

            # 2. Primary + Secondary
            clean_snr2, noise_snr2, noisy_snr2, target_level2 = segmental_snr_mixer(params=params, 
                                                                    clean=chose_primary, 
                                                                    noise=clean2, 
                                                                    snr=snr2)
            # 3. Primary + Seconday (clean2) + Noise
            clean_snr3, noise_snr3, noisy_snr3, target_level3 = segmental_snr_mixer(params=params, 
                                                                    clean=noisy_snr2, 
                                                                    noise=noise, 
                                                                    snr=snr3)
            # unexpected clipping
            #if is_clipped(clean_snr) or is_clipped(noise_snr2) or is_clipped(noisy_snr2):
            if is_clipped(clean_snr) or is_clipped(noisy_snr):
                print("Warning: File #" + str(file_num) + " has unexpected clipping, " + \
                    "returning without writing audio to disk")
                continue

            if is_clipped(clean_snr2) or is_clipped(noisy_snr2):
                print("Warning: File #" + str(file_num) + " has unexpected clipping, " + \
                    "returning without writing audio to disk")
                continue


            if is_clipped(clean_snr3) or is_clipped(noisy_snr3):
                print("Warning: File #" + str(file_num) + " has unexpected clipping, " + \
                    "returning without writing audio to disk")
                continue

            clean_source_files += clean_sf
            noise_source_files += noise_sf

            # write resultant audio streams to files
            hyphen = '-'
            clean_source_filenamesonly = [i[:-4].split(os.path.sep)[-1] for i in clean_sf]
            clean_files_joined = hyphen.join(clean_source_filenamesonly)[:MAXFILELEN]
            noise_source_filenamesonly = [i[:-4].split(os.path.sep)[-1] for i in noise_sf]
            noise_files_joined = hyphen.join(noise_source_filenamesonly)[:MAXFILELEN]

            noisyfilename = 'primary_noisy_fileid_' + str(file_num) + '_' + clean_files_joined + '_' + noise_files_joined + '_snr' + \
                            str(snr) + '_tl' + str(target_level) + '.wav'

            cleanfilename = 'clean_fileid_'+str(file_num)+'.wav'
            noisefilename = 'noise_fileid_'+str(file_num)+'.wav'

            noisypath = os.path.join(params['noisyspeech_dir'], noisyfilename)
            cleanpath = os.path.join(params['clean_proc_dir'], cleanfilename)
            noisepath = os.path.join(params['noise_proc_dir'], noisefilename)

            noisyfilename2 = 'ps_noisy_fileid_'+ str(file_num) + '_' +  clean_files_joined + '_' + noise_files_joined + '_snr' + \
                            str(snr) + '_tl' + str(target_level) + '.wav'
            cleanfilename2 = 'ps_clean_fileid_'+str(file_num)+'.wav'
            noisefilename2 = 'ps_noise_fileid_'+str(file_num)+'.wav'

            noisypath2 = os.path.join(params['noisyspeech_dir'], noisyfilename2)
            cleanpath2 = os.path.join(params['clean_proc_dir'], cleanfilename2)
            noisepath2 = os.path.join(params['noise_proc_dir'], noisefilename2)

            noisyfilename3 = 'psn_noisy_fileid_' + str(file_num) + '_' +clean_files_joined + '_' + noise_files_joined + '_snr' + \
                            str(snr) + '_tl' + str(target_level) + '.wav'
            cleanfilename3 = 'psn_clean_fileid_'+str(file_num)+'.wav'
            noisefilename3 = 'psn_noise_fileid_'+str(file_num)+'.wav'

            noisypath3 = os.path.join(params['noisyspeech_dir'], noisyfilename3)
            cleanpath3 = os.path.join(params['clean_proc_dir'], cleanfilename3)
            noisepath3 = os.path.join(params['noise_proc_dir'], noisefilename3)

            audio_signals = [noisy_snr, clean_snr, noise_snr]
            file_paths = [noisypath, cleanpath, noisepath]

            audio_signals2 = [noisy_snr2, clean_snr, noise_snr2]
            file_paths2 = [noisypath2, cleanpath2, noisepath2]

            audio_signals3 = [noisy_snr3, clean_snr, noise_snr3]
            file_paths3 = [noisypath3, cleanpath3, noisepath3]

            file_num += 1 #         file_num = file_num + 3*num_clips

            for i in range(len(audio_signals)):
                try:
                    audiowrite(file_paths[i], audio_signals[i], params['fs'])
                    audiowrite(file_paths2[i], audio_signals2[i], params['fs'])
                    audiowrite(file_paths3[i], audio_signals3[i], params['fs'])
                except Exception as e:
                    print(str(e))

            # for i in range(len(audio_signals2)):
            #     try:
            #     except Exception as e:
            #         print(str(e))

            # for i in range(len(audio_signals3)):
            #     try:
            #         audiowrite(file_paths3[i], audio_signals3[i], params['fs'])
            #     except Exception as e:
            #         print(str(e))

    return clean_source_files, clean_clipped_files, clean_low_activity_files, \
                noise_source_files, noise_clipped_files, noise_low_activity_files

def main_body():
    '''Main body of this file'''

    parser = argparse.ArgumentParser()

    # Configurations: read noisyspeech_synthesizer.cfg and gather inputs
    parser.add_argument('--cfg', default='pdns_synthesizer_icassp2022.cfg',
                        help='Read noisyspeech_synthesizer.cfg for all the details')
    parser.add_argument('--cfg_str', type=str, default='noisy_speech')
    args = parser.parse_args()

    params = dict()
    params['args'] = args
    cfgpath = os.path.join(args.cfg)
    # os.path.join(os.path.dirname(__file__), args.cfg)
    assert os.path.exists(cfgpath), f'No configuration file as [{cfgpath}]'

    cfg = CP.ConfigParser()
    cfg._interpolation = CP.ExtendedInterpolation()
    cfg.read(cfgpath)
    params['cfg'] = cfg._sections[args.cfg_str]
    cfg = params['cfg']

    clean_dir = os.path.join('datasets/clean')

    if cfg['speech_dir'] != 'None':
        clean_dir = cfg['speech_dir']
        
    if not os.path.exists(clean_dir):
        assert False, ('Clean speech data is required')

    if cfg['speech_dir2'] != 'None':
        clean_dir2 = cfg['speech_dir2']

    if cfg['spkid_csv'] != 'None':
        spkid_csv = cfg['spkid_csv']

    if not os.path.exists(clean_dir2):
        assert False, ('Clean speech2 data is required')

    if cfg['rir_dir'] != 'None':
        rir_dir = cfg['rir_dir']

    if cfg['noise_dir'] != 'None':
        noise_dir = cfg['noise_dir']
    if not os.path.exists(noise_dir):
        assert False, ('Clean speech data is required')
        
    print(clean_dir)
    print(clean_dir2)
    print(noise_dir)
    print(spkid_csv)
    print(rir_dir)

    if cfg['noise_dir'] != 'None':
        noise_dir = cfg['noise_dir']
    if not os.path.exists:
        assert False, ('Noise data is required')

    params['fs'] = int(cfg['sampling_rate'])
    params['audioformat'] = cfg['audioformat']
    params['audio_length'] = float(cfg['audio_length'])
    params['silence_length'] = float(cfg['silence_length'])
    params['total_hours'] = float(cfg['total_hours'])
    
    # clean singing speech
    params['clean_singing'] = str(cfg['clean_singing'])
    params['singing_choice'] = int(cfg['singing_choice'])

    # rir
    params['rir_choice'] = int(cfg['rir_choice'])
    params['lower_t60'] = float(cfg['lower_t60'])
    params['upper_t60'] = float(cfg['upper_t60'])
    params['rir_table_csv'] = str(cfg['rir_table_csv'])
    params['clean_speech_t60_csv'] = str(cfg['clean_speech_t60_csv'])

    if cfg['fileindex_start'] != 'None' and cfg['fileindex_start'] != 'None':
        params['num_files'] = int(cfg['fileindex_end'])-int(cfg['fileindex_start'])
        params['fileindex_start'] = int(cfg['fileindex_start'])
        params['fileindex_end'] = int(cfg['fileindex_end'])
    else:
        params['num_files'] = int((params['total_hours']*60*60)/params['audio_length'])
        params['fileindex_start'] = 0
        params['fileindex_end'] = int(params['num_files'])

    print('Number of files to be synthesized:', params['num_files'])
    
    params['is_test_set'] = utils.str2bool(cfg['is_test_set'])
    params['clean_activity_threshold'] = float(cfg['clean_activity_threshold'])
    params['noise_activity_threshold'] = float(cfg['noise_activity_threshold'])
    params['snr_lower'] = int(cfg['snr_lower'])
    params['snr_upper'] = int(cfg['snr_upper'])
    
    params['randomize_snr'] = utils.str2bool(cfg['randomize_snr'])
    params['target_level_lower'] = int(cfg['target_level_lower'])
    params['target_level_upper'] = int(cfg['target_level_upper'])
    
    if 'snr' in cfg.keys():
        params['snr'] = int(cfg['snr'])
    else:
        params['snr'] = int((params['snr_lower'] + params['snr_upper'])/2)

    params['noisyspeech_dir'] = utils.get_dir(cfg, 'noisy_destination', 'noisy')
    params['clean_proc_dir'] = utils.get_dir(cfg, 'clean_destination', 'clean')
    params['noise_proc_dir'] = utils.get_dir(cfg, 'noise_destination', 'noise')

    if 'speech_csv' in cfg.keys() and cfg['speech_csv'] != 'None':
        cleanfilenames = pd.read_csv(cfg['speech_csv'])
        cleanfilenames = cleanfilenames['filename']
    else:
        cleanfilenames= []
        for path in Path(cfg['speech_dir']).rglob('*.wav'):
            cleanfilenames.append(str(path.resolve()))

    selected_primary=[]
    selected_secondary=[]

    with open(spkid_csv, 'r') as file:
        my_reader = csv.reader(file, delimiter=',')
        for row in my_reader:
            if row[1]== 'primary':
                selected_primary.append(row)
            elif row[1]== 'secondary':
                selected_secondary.append(row)

    cleanfilenames = []
    for row in selected_primary:
        cleanfilenames.append(row[0])

    cleanfilenames2 = []
    for row in selected_secondary:
        cleanfilenames2.append(row[0])
    
    params['cleanfilenames'] = cleanfilenames

    shuffle(cleanfilenames2)
    params['cleanfilenames2'] =cleanfilenames2

    rirfilenames= []
    for path in Path(cfg['rir_dir']).rglob('*.wav'):
        rirfilenames.append(str(path.resolve()))

    shuffle(rirfilenames)
    params['myrir'] = rirfilenames
    
    if 'noise_csv' in cfg.keys() and cfg['noise_csv'] != 'None':
        noisefilenames = pd.read_csv(cfg['noise_csv'])
        noisefilenames = noisefilenames['filename']
    else:
        noisefilenames = glob.glob(os.path.join(noise_dir, params['audioformat']))

    if len(noisefilenames)!=0:
        shuffle(noisefilenames)
        params['noisefilenames'] = noisefilenames
    else:
        noisedirs = glob.glob(os.path.join(noise_dir, '*'))
        if cfg['noise_types_excluded'] != 'None':
            dirstoexclude = cfg['noise_types_excluded'].split(',')
            for dirs in dirstoexclude:
                noisedirs.remove(dirs)
        shuffle(noisedirs)
        params['noisedirs'] = noisedirs

    # Call main_gen() to generate audio
    clean_source_files, clean_clipped_files, clean_low_activity_files, \
    noise_source_files, noise_clipped_files, noise_low_activity_files = main_gen(params)

    # Create log directory if needed, and write log files of clipped and low activity files
    log_dir = utils.get_dir(cfg, 'log_dir', 'Logs')

    utils.write_log_file(log_dir, 'source_files.csv', clean_source_files + noise_source_files)
    utils.write_log_file(log_dir, 'clipped_files.csv', clean_clipped_files + noise_clipped_files)
    utils.write_log_file(log_dir, 'low_activity_files.csv', \
                         clean_low_activity_files + noise_low_activity_files)

    # Compute and print stats about percentange of clipped and low activity files
    total_clean = len(clean_source_files) + len(clean_clipped_files) + len(clean_low_activity_files)
    total_noise = len(noise_source_files) + len(noise_clipped_files) + len(noise_low_activity_files)

    pct_clean_clipped = round(len(clean_clipped_files)/total_clean*100, 1)
    pct_noise_clipped = round(len(noise_clipped_files)/total_noise*100, 1)
    pct_clean_low_activity = round(len(clean_low_activity_files)/total_clean*100, 1)
    pct_noise_low_activity = round(len(noise_low_activity_files)/total_noise*100, 1)

    print("Of the " + str(total_clean) + " clean speech files analyzed, " + \
          str(pct_clean_clipped) + "% had clipping, and " + str(pct_clean_low_activity) + \
          "% had low activity " + "(below " + str(params['clean_activity_threshold']*100) + \
          "% active percentage)")
    print("Of the " + str(total_noise) + " noise files analyzed, " + str(pct_noise_clipped) + \
          "% had clipping, and " + str(pct_noise_low_activity) + "% had low activity " + \
          "(below " + str(params['noise_activity_threshold']*100) + "% active percentage)")

if __name__ == '__main__':

    main_body()

          # clean_clipped_files += clean_cf
        # clean_low_activity_files += clean_laf

        # clean_clipped_files2 += clean_cf2
        # clean_low_activity_files2 += clean_laf2    
        
        # noise_clipped_files += noise_cf
        # noise_low_activity_files += noise_laf

        # get rir files and config

        # mix clean speech and noise      
        
        # Uncomment the below lines if you need segmental SNR and comment the above lines using snr_mixer
        #clean_snr, noise_snr, noisy_snr, target_level = segmental_snr_mixer(params=params, 
        #                                                         clean=clean, 
        #                                                          noise=noise, 
        #                                                         snr=snr)
# def main_body():
#     '''Main body of this file'''

#     parser = argparse.ArgumentParser()

#     # Configurations: read noisyspeech_synthesizer.cfg and gather inputs
#     parser.add_argument('--cfg', default='pdns_synthesizer_icassp2022.cfg',
#                         help='Read noisyspeech_synthesizer.cfg for all the details')
#     parser.add_argument('--cfg_str', type=str, default='noisy_speech')
#     args = parser.parse_args()

#     params = dict()
#     params['args'] = args
#     cfgpath = os.path.join('/mnt/f/4th_DNSChallenge/ICASSP_2022/DNS-Challenge',args.cfg)
#     # os.path.join(os.path.dirname(__file__), args.cfg)
#     assert os.path.exists(cfgpath), f'No configuration file as [{cfgpath}]'

#     cfg = CP.ConfigParser()
#     cfg._interpolation = CP.ExtendedInterpolation()
#     cfg.read(cfgpath)
#     params['cfg'] = cfg._sections[args.cfg_str]
#     cfg = params['cfg']

#     ROOT_DIR ='/mnt/f/4th_DNSChallenge/ICASSP_2022/DNS-Challenge' 
#     clean_dir = os.path.join(ROOT_DIR, 'datasets/clean')
# #    clean_dir = os.path.join(os.path.dirname(__file__), 'datasets/clean')

#     if cfg['speech_dir'] != 'None':
#         clean_dir = cfg['speech_dir']
        
#     if not os.path.exists(clean_dir):
#         assert False, ('Clean speech data is required')

    # if cfg['speech_dir2'] != 'None':
    #     clean_dir2 = cfg['speech_dir2']

    # if cfg['spkid_csv'] != 'None':
    #     spkid_csv = cfg['spkid_csv']

    # if not os.path.exists(clean_dir2):
    #     assert False, ('Clean speech2 data is required')

    # if cfg['rir_dir'] != 'None':
    #     rir_dir = cfg['rir_dir']

    # if cfg['noise_dir'] != 'None':
    #     noise_dir = cfg['noise_dir']
    # if not os.path.exists(noise_dir):
    #     assert False, ('Clean speech data is required')
        
    # #noise_dir = os.path.join(os.path.dirname(__file__), 'datasets/noise')
    # print(clean_dir)
    # print(clean_dir2)
    # print(noise_dir)
    # print(spkid_csv)
    # print(rir_dir)

#     if cfg['noise_dir'] != 'None':
#         noise_dir = cfg['noise_dir']
#     if not os.path.exists:
#         assert False, ('Noise data is required')

#     params['fs'] = int(cfg['sampling_rate'])
#     params['audioformat'] = cfg['audioformat']
#     params['audio_length'] = float(cfg['audio_length'])
#     params['silence_length'] = float(cfg['silence_length'])
#     params['total_hours'] = float(cfg['total_hours'])
    
#     # clean singing speech
#     params['clean_singing'] = str(cfg['clean_singing'])
#     params['singing_choice'] = int(cfg['singing_choice'])
# #    params['use_singing_data'] = bool(cfg['use_singing_data'])

#     # rir
#     params['rir_choice'] = int(cfg['rir_choice'])
#     params['lower_t60'] = float(cfg['lower_t60'])
#     params['upper_t60'] = float(cfg['upper_t60'])
#     params['rir_table_csv'] = str(cfg['rir_table_csv'])
#     params['clean_speech_t60_csv'] = str(cfg['clean_speech_t60_csv'])

    # if cfg['fileindex_start'] != 'None' and cfg['fileindex_start'] != 'None':
    #     params['num_files'] = int(cfg['fileindex_end'])-int(cfg['fileindex_start'])
    #     params['fileindex_start'] = int(cfg['fileindex_start'])
    #     params['fileindex_end'] = int(cfg['fileindex_end'])
    # else:
    #     params['num_files'] = int((params['total_hours']*60*60)/params['audio_length'])
    #     params['fileindex_start'] = 0
    #     params['fileindex_end'] = int(params['num_files'])

    # print('Number of files to be synthesized:', params['num_files'])
    
    # params['is_test_set'] = utils.str2bool(cfg['is_test_set'])
    # params['clean_activity_threshold'] = float(cfg['clean_activity_threshold'])
    # params['noise_activity_threshold'] = float(cfg['noise_activity_threshold'])
    # params['snr_lower'] = int(cfg['snr_lower'])
    # params['snr_upper'] = int(cfg['snr_upper'])
    
    # params['randomize_snr'] = utils.str2bool(cfg['randomize_snr'])
    # params['target_level_lower'] = int(cfg['target_level_lower'])
    # params['target_level_upper'] = int(cfg['target_level_upper'])
    
    # if 'snr' in cfg.keys():
    #     params['snr'] = int(cfg['snr'])
    # else:
    #     params['snr'] = int((params['snr_lower'] + params['snr_upper'])/2)

    # params['noisyspeech_dir'] = utils.get_dir(cfg, 'noisy_destination', 'noisy')
    # params['clean_proc_dir'] = utils.get_dir(cfg, 'clean_destination', 'clean')
    # params['noise_proc_dir'] = utils.get_dir(cfg, 'noise_destination', 'noise')

    # if 'speech_csv' in cfg.keys() and cfg['speech_csv'] != 'None':
    #     cleanfilenames = pd.read_csv(cfg['speech_csv'])
    #     cleanfilenames = cleanfilenames['filename']
    # else:
    #     cleanfilenames= []
    #     for path in Path(cfg['speech_dir']).rglob('*.wav'):
    #         cleanfilenames.append(str(path.resolve()))

    # selected_primary=[]
    # selected_secondary=[]

    # with open(spkid_csv, 'r') as file:
    #     my_reader = csv.reader(file, delimiter=',')
    #     for row in my_reader:
    #         if row[1]== 'primary':
    #             selected_primary.append(row)
    #         elif row[1]== 'secondary':
    #             selected_secondary.append(row)

    # primary_spks =[]
    # primary_spkids =[]

    # for row in selected_primary:
    #     primary_spks.append(os.path.join(clean_dir,row[0])) 
    #     primary_spkids.append(row[1])

    # secondary_spks =[]
    # for row in selected_secondary:
    #     secondary_spks.append(os.path.join(clean_dir,row[0])) 

    # cleanfilenames = primary_spks
    # cleanfilenames2 = secondary_spks
    
    # params['cleanfilenames'] = cleanfilenames
    # params['primary_spkids'] = primary_spkids
    # params['primary_spks'] = primary_spks

    # shuffle(secondary_spks)
    # params['secondary_spks'] = secondary_spks

    # shuffle(cleanfilenames2)
    # params['cleanfilenames2'] =cleanfilenames2

    # rirfilenames= []
    # for path in Path(cfg['rir_dir']).rglob('*.wav'):
    #     rirfilenames.append(str(path.resolve()))

    # shuffle(rirfilenames)
    # params['myrir'] = rirfilenames

    # params['num_cleanfiles2'] = len(params['cleanfilenames2'])

    # params['spk_count'] = len(list(set(primary_spkids)))

    # params['num_perspk'] = int(params['num_files']/params['spk_count'])

""" def build_audio3(is_clean, params, spk_index, audio_samples_length=-1):
    '''Construct an audio signal from source files
    Return list of all audio chuncks for primary speakers'''

    fs_output = params['fs']
    silence_length = params['silence_length']

    if audio_samples_length == -1:
        audio_samples_length = int(params['audio_length']*params['fs'])

    output_audio = np.zeros(0)
    remaining_length = audio_samples_length
    files_used = []
    clipped_files = []

    if is_clean:
        source_files = params['cleanfilenames']
        idx = spk_index

    input_audio, fs_input = audioread(source_files[idx])
    audio_length= params['audio_length']*fs_input

    if fs_input != fs_output:
        input_audio = librosa.resample(input_audio, fs_input, fs_output)
    
    num_seg= int(input_audio.shape[0]/(audio_length))
    #chosen_idx = 0 

    audios_all=[]
    idx_seg = 0 

    for seg in range(0,num_seg):
        print(seg)
        temp_audio = input_audio[int(seg*audio_length) : int((seg + 1)*audio_length)]

        if not is_clipped(temp_audio):
            audios_all.append(temp_audio)
        else:
            print(' audioo is clipped')

    return audios_all
    # output_audio, files_used, clipped_files, idx
 """
""" def build_audio(is_clean, params, index, audio_samples_length=-1):
    '''Construct an audio signal from source files'''

    fs_output = params['fs']
    silence_length = params['silence_length']
    if audio_samples_length == -1:
        audio_samples_length = int(params['audio_length']*params['fs'])

    output_audio = np.zeros(0)
    remaining_length = audio_samples_length
    files_used = []
    clipped_files = []

    if is_clean:
        source_files = params['cleanfilenames']
        idx = index
    else:
        if 'noisefilenames' in params.keys():
            source_files = params['noisefilenames']
            idx = index
        # if noise files are organized into individual subdirectories, pick a directory randomly
        else:
            noisedirs = params['noisedirs']
            # pick a noise category randomly
            idx_n_dir = np.random.randint(0, np.size(noisedirs))
            source_files = glob.glob(os.path.join(noisedirs[idx_n_dir], 
                                                  params['audioformat']))
            shuffle(source_files)
            # pick a noise source file index randomly
            idx = np.random.randint(0, np.size(source_files))

    # initialize silence
    silence = np.zeros(int(fs_output*silence_length))

    # iterate through multiple clips until we have a long enough signal
    tries_left = MAXTRIES
    while remaining_length > 0 and tries_left > 0:

        # read next audio file and resample if necessary
        idx = (idx + 1) % np.size(source_files)

        input_audio, fs_input = audioread(source_files[idx])
        if fs_input != fs_output:
            input_audio = librosa.resample(input_audio, fs_input, fs_output)

        # if current file is longer than remaining desired length, and this is
        # noise generation or this is training set, subsample it randomly
        if len(input_audio) > remaining_length and (not is_clean or params['is_test_set']):
#         if len(input_audio) > remaining_length and (not is_clean or not params['is_test_set']):

            idx_seg = np.random.randint(0, len(input_audio)-remaining_length)
            input_audio = input_audio[idx_seg:idx_seg+remaining_length]

        # check for clipping, and if found move onto next file
        if is_clipped(input_audio):
            clipped_files.append(source_files[idx])
            tries_left -= 1
            continue

        # concatenate current input audio to output audio stream
        files_used.append(source_files[idx])
        output_audio = np.append(output_audio, input_audio)
        remaining_length -= len(input_audio)

        # add some silence if we have not reached desired audio length
        if remaining_length > 0:
            silence_len = min(remaining_length, len(silence))
            output_audio = np.append(output_audio, silence[:silence_len])
            remaining_length -= silence_len

    if tries_left == 0 and not is_clean and 'noisedirs' in params.keys():
        print("There are not enough non-clipped files in the " + noisedirs[idx_n_dir] + \
              " directory to complete the audio build")
        return [], [], clipped_files, idx

    return output_audio, files_used, clipped_files, idx
 """
""" def build_audio2(is_clean, params, index, audio_samples_length=-1):
    '''Construct an audio signal from source files'''

    fs_output = params['fs']
    silence_length = params['silence_length']
    
    if audio_samples_length == -1:
        audio_samples_length = int(params['audio_length']*params['fs'])

    output_audio = np.zeros(0)
    remaining_length = audio_samples_length
    files_used = []
    clipped_files = []

    if is_clean:
        source_files = params['cleanfilenames']
        idx = index
    else:
        if 'noisefilenames' in params.keys():
            source_files = params['noisefilenames']
            idx = index
        # if noise files are organized into individual subdirectories, pick a directory randomly
        else:
            noisedirs = params['cleanfilenames2']
            #params['noisedirs']
            # pick a noise category randomly
            idx_n_dir = np.random.randint(0, len(noisedirs))
            source_files = noisedirs
            #glob.glob(os.path.join(noisedirs[idx_n_dir], params['audioformat']))
            shuffle(source_files)
            # pick a noise source file index randomly
            idx = np.random.randint(0, np.size(source_files))

    # initialize silence
    silence = np.zeros(int(fs_output*silence_length))

    # iterate through multiple clips until we have a long enough signal
    tries_left = MAXTRIES
    while remaining_length > 0 and tries_left > 0:

        # read next audio file and resample if necessary
        idx = (idx + 1) % np.size(source_files)
        input_audio, fs_input = audioread(source_files[idx])
        if fs_input != fs_output:
            input_audio = librosa.resample(input_audio, fs_input, fs_output)

        # if current file is longer than remaining desired length, and this is
        # noise generation or this is training set, subsample it randomly
        if len(input_audio) > remaining_length and (not is_clean or params['is_test_set']):
#         if len(input_audio) > remaining_length and (not is_clean or not params['is_test_set']):

            idx_seg = np.random.randint(0, len(input_audio)-remaining_length)
            input_audio = input_audio[idx_seg:idx_seg+remaining_length]

        # check for clipping, and if found move onto next file
        if is_clipped(input_audio):
            clipped_files.append(source_files[idx])
            tries_left -= 1
            continue

        # concatenate current input audio to output audio stream
        files_used.append(source_files[idx])
        output_audio = np.append(output_audio, input_audio)
        remaining_length -= len(input_audio)

        # add some silence if we have not reached desired audio length
        if remaining_length > 0:
            silence_len = min(remaining_length, len(silence))
            output_audio = np.append(output_audio, silence[:silence_len])
            remaining_length -= silence_len

    if tries_left == 0 and not is_clean and 'noisedirs' in params.keys():
        print("There are not enough non-clipped files in the " + noisedirs[idx_n_dir] + \
              " directory to complete the audio build")
        return [], [], clipped_files, idx

    return output_audio, files_used, clipped_files, idx

def gen_audio(is_clean, params, index, audio_samples_length=-1):
    '''Calls build_audio() to get an audio signal, and verify that it meets the
       activity threshold'''

    clipped_files = []
    low_activity_files = []
    if audio_samples_length == -1:
        audio_samples_length = int(params['audio_length']*params['fs'])
    
    if is_clean:
        activity_threshold = params['clean_activity_threshold']
    else:
        activity_threshold = params['noise_activity_threshold']

    while True:
        audio, source_files, new_clipped_files, index = \
            build_audio(is_clean, params, index, audio_samples_length)

        clipped_files += new_clipped_files
        if len(audio) < audio_samples_length:
            continue

        if activity_threshold == 0.0:
            break

        percactive = activitydetector(audio=audio)
        if percactive > activity_threshold:
            break
        else:
            low_activity_files += source_files
    return audio, source_files, clipped_files, low_activity_files, index
 """

""" def gen_audio2(is_clean, params, index, audio_samples_length=-1):
    '''Calls build_audio() to get an audio signal, and verify that it meets the
       activity threshold'''

    clipped_files = []
    low_activity_files = []
    if audio_samples_length == -1:
        audio_samples_length = int(params['audio_length']*params['fs'])
    
    if is_clean:
        activity_threshold = params['clean_activity_threshold']
    else:
        activity_threshold = params['noise_activity_threshold']

    while True:
        audio, source_files, new_clipped_files, index = \
            build_audio2(is_clean, params, index, audio_samples_length)

        clipped_files += new_clipped_files
        if len(audio) < audio_samples_length:
            continue

        if activity_threshold == 0.0:
            break

        percactive = activitydetector(audio=audio)
        if percactive > activity_threshold:
            break
        else:
            low_activity_files += source_files

    return audio, source_files, clipped_files, low_activity_files, index
 """
