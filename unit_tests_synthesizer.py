import numpy as np
import soundfile as sf
import glob
import argparse
import os
import utils
import configparser as CP

LOW_ENERGY_THRESH = -60

def test_snr(clean, noise, expected_snr, snrtolerance=2):
    '''Test for SNR
    Note: It is not applicable for Segmental SNR'''
    rmsclean = (clean**2).mean()**0.5
    rmsnoise = (noise**2).mean()**0.5
    actual_snr = 20*np.log10(rmsclean/rmsnoise)
    return actual_snr > (expected_snr-snrtolerance) and actual_snr < (expected_snr+snrtolerance)

def test_normalization(audio, expected_rms=-25, normtolerance=2):
    '''Test for Normalization
    Note: Set it to False if different target levels are used'''
    rmsaudio = (audio**2).mean()**0.5
    rmsaudiodb = 20*np.log10(rmsaudio)
    return rmsaudiodb > (expected_rms-normtolerance) and rmsaudiodb < (expected_rms+normtolerance)

def test_samplingrate(sr, expected_sr=16000):
    '''Test to ensure all clips have same sampling rate'''
    return expected_sr == sr

def test_clipping(audio, num_consecutive_samples=3, clipping_threshold=0.01):
    '''Test to detect clipping'''
    clipping = False
    for i in range(0, len(audio)-num_consecutive_samples-1):
        audioseg = audio[i:i+num_consecutive_samples]
        if abs(max(audioseg)-min(audioseg)) < clipping_threshold or abs(max(audioseg)) >= 1:
            clipping = True
            break
    return clipping

def test_zeros_beg_end(audio, num_zeros=16000, low_energy_thresh=LOW_ENERGY_THRESH):
    '''Test if there are zeros in the beginning and the end of the signal'''
    beg_segment_energy = 20*np.log10(audio[:num_zeros]**2).mean()**0.5
    end_segment_energy = 20*np.log10(audio[-num_zeros:]**2).mean()**0.5
    return beg_segment_energy < low_energy_thresh or end_segment_energy < low_energy_thresh

def adsp_filtering_test(adsp, without_adsp):
    diff = adsp - without_adsp
    if any(val >0.0001 for val in diff):
        
    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', default='noisyspeech_synthesizer.cfg')
    parser.add_argument('--cfg_str', type=str, default='noisy_speech')

    args = parser.parse_args()
    
    cfgpath = os.path.join(os.path.dirname(__file__), args.cfg)
    assert os.path.exists(cfgpath), f'No configuration file as [{cfgpath}]'

    cfg = CP.ConfigParser()
    cfg._interpolation = CP.ExtendedInterpolation()
    cfg.read(cfgpath)
    cfg = cfg._sections[args.cfg_str]
    
    noisydir = cfg['noisy_train']
    cleandir = cfg['clean_train']
    noisedir = cfg['noise_train']
    audioformat = cfg['audioformat']
    
    # List of noisy speech files
    noisy_speech_filenames_big = glob.glob(os.path.join(noisydir, audioformat))
    noisy_speech_filenames = noisy_speech_filenames_big[0:10]
    # Initialize the lists
    noisy_filenames_list = []
    clean_filenames_list = []
    noise_filenames_list = []
    snr_results_list =[]
    clean_norm_results_list = []
    noise_norm_results_list = []
    noisy_norm_results_list = []
    clean_sr_results_list = []
    noise_sr_results_list = []
    noisy_sr_results_list = []
    clean_clipping_results_list = []
    noise_clipping_results_list = []
    noisy_clipping_results_list = []

    skipped_string = 'Skipped'
    # Initialize the counters for stats
    total_clips = len(noisy_speech_filenames)


    for noisypath in noisy_speech_filenames:
        # To do: add right paths to clean filename and noise filename
        noisy_filename = os.path.basename(noisypath)
        clean_filename = 'clean_fileid_'+os.path.splitext(noisy_filename)[0].split('fileid_')[1]+'.wav'
        cleanpath = os.path.join(cleandir, clean_filename)
        noise_filename = 'noise_fileid_'+os.path.splitext(noisy_filename)[0].split('fileid_')[1]+'.wav'
        noisepath = os.path.join(noisedir, noise_filename)

        noisy_filenames_list.append(noisy_filename)
        clean_filenames_list.append(clean_filename)
        noise_filenames_list.append(noise_filename)

        # Read clean, noise and noisy signals
        clean_signal, fs_clean = sf.read(cleanpath)
        noise_signal, fs_noise = sf.read(noisepath)
        noisy_signal, fs_noisy = sf.read(noisypath)

        # SNR Test
        # To do: add right path split to extract SNR
        if utils.str2bool(cfg['snr_test']):
            snr = int(noisy_filename.split('_snr')[1].split('_')[0])
            snr_results_list.append(str(test_snr(clean=clean_signal, \
             noise=noise_signal, expected_snr=snr)))
        else:
            snr_results_list.append(skipped_string)
        
        # Normalization test
        if utils.str2bool(cfg['norm_test']):
            tl = int(noisy_filename.split('_tl')[1].split('_')[0])
            clean_norm_results_list.append(str(test_normalization(clean_signal)))
            noise_norm_results_list.append(str(test_normalization(noise_signal)))
            noisy_norm_results_list.append(str(test_normalization(noisy_signal, expected_rms=tl)))
        else:
            clean_norm_results_list.append(skipped_string)
            noise_norm_results_list.append(skipped_string)
            noisy_norm_results_list.append(skipped_string)
        
        # Sampling rate test
        if utils.str2bool(cfg['sampling_rate_test']):
            clean_sr_results_list.append(str(test_samplingrate(sr=fs_clean)))
            noise_sr_results_list.append(str(test_samplingrate(sr=fs_noise)))
            noisy_sr_results_list.append(str(test_samplingrate(sr=fs_noisy)))
        else:
            clean_sr_results_list.append(skipped_string)
            noise_sr_results_list.append(skipped_string)
            noisy_sr_results_list.append(skipped_string)
        
        # Clipping test
        if utils.str2bool(cfg['clipping_test']):
            clean_clipping_results_list.append(str(test_clipping(audio=clean_signal)))
            noise_clipping_results_list.append(str(test_clipping(audio=noise_signal)))
            noisy_clipping_results_list.append(str(test_clipping(audio=noisy_signal)))
        else:
            clean_clipping_results_list.append(skipped_string)
            noise_clipping_results_list.append(skipped_string)
            noisy_clipping_results_list.append(skipped_string)

    # Stats
    pc_snr_passed = round(snr_results_list.count('True')/total_clips*100, 1)
    pc_clean_norm_passed = round(clean_norm_results_list.count('True')/total_clips*100, 1)
    pc_noise_norm_passed = round(noise_norm_results_list.count('True')/total_clips*100, 1)
    pc_noisy_norm_passed = round(noisy_norm_results_list.count('True')/total_clips*100, 1)
    pc_clean_sr_passed = round(clean_sr_results_list.count('True')/total_clips*100, 1)
    pc_noise_sr_passed = round(noise_sr_results_list.count('True')/total_clips*100, 1)
    pc_noisy_sr_passed = round(noisy_sr_results_list.count('True')/total_clips*100, 1)
    pc_clean_clipping_passed = round(clean_clipping_results_list.count('True')/total_clips*100, 1)
    pc_noise_clipping_passed = round(noise_clipping_results_list.count('True')/total_clips*100, 1)
    pc_noisy_clipping_passed = round(noisy_clipping_results_list.count('True')/total_clips*100, 1)

    print('% clips that passed SNR test:', pc_snr_passed)
    
    print('% clean clips that passed Normalization tests:', pc_clean_norm_passed)
    print('% noise clips that passed Normalization tests:', pc_noise_norm_passed)
    print('% noisy clips that passed Normalization tests:', pc_noisy_norm_passed)

    print('% clean clips that passed Sampling Rate tests:', pc_clean_sr_passed)
    print('% noise clips that passed Sampling Rate tests:', pc_noise_sr_passed)
    print('% noisy clips that passed Sampling Rate tests:', pc_noisy_sr_passed)

    print('% clean clips that passed Clipping tests:', pc_clean_clipping_passed)
    print('% noise clips that passed Clipping tests:', pc_noise_clipping_passed)
    print('% noisy clips that passed Clipping tests:', pc_noisy_clipping_passed)

    log_dir = utils.get_dir(cfg, 'unit_tests_log_dir', 'Unit_tests_logs')
    
    if not os.path.exists(log_dir):
        log_dir = os.path.join(os.path.dirname(__file__), 'Unit_tests_logs')
        os.makedirs(log_dir)
    
    utils.write_log_file(log_dir, 'unit_test_results.csv', [noisy_filenames_list, clean_filenames_list, \
                            noise_filenames_list, snr_results_list, clean_norm_results_list, noise_norm_results_list, \
                            noisy_norm_results_list, clean_sr_results_list, noise_sr_results_list, noisy_sr_results_list, \
                            clean_clipping_results_list, noise_clipping_results_list, noisy_clipping_results_list])