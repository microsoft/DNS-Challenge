#!/usr/bin/bash

# ***** Datasets for ICASSP 2023 DNS Challenge 5 - Personalized DNS Track *****

# NOTE: Before downloading, make sure you have enough space
# on your local storage!

# In all, you will need about 380TB to store the UNPACKED data.
# Archived, the same data takes about 200GB total.

# Please comment out the files you don't need before launching
# the script.

# NOTE: By default, the script *DOES NOT* DOWNLOAD ANY FILES!
# Please scroll down and edit this script to pick the
# downloading method that works best for you.

# -------------------------------------------------------------

BLOB_NAMES=(
    V5_training_dataset/Track1_Headset/VocalSet_48kHz_mono.tgz

    V5_training_dataset/Track1_Headset/vctk_wav48_silence_trimmed.tgz.partac
    V5_training_dataset/Track1_Headset/vctk_wav48_silence_trimmed.tgz.partab
    V5_training_dataset/Track1_Headset/vctk_wav48_silence_trimmed.tgz.partaa

    V5_training_dataset/Track1_Headset/russian_speech.tgz

    V5_training_dataset/Track1_Headset/read_speech.tgz.partau
    V5_training_dataset/Track1_Headset/read_speech.tgz.partat
    V5_training_dataset/Track1_Headset/read_speech.tgz.partas
    V5_training_dataset/Track1_Headset/read_speech.tgz.partar
    V5_training_dataset/Track1_Headset/read_speech.tgz.partaq
    V5_training_dataset/Track1_Headset/read_speech.tgz.partap
    V5_training_dataset/Track1_Headset/read_speech.tgz.partao
    V5_training_dataset/Track1_Headset/read_speech.tgz.partan
    V5_training_dataset/Track1_Headset/read_speech.tgz.partam
    V5_training_dataset/Track1_Headset/read_speech.tgz.partal
    V5_training_dataset/Track1_Headset/read_speech.tgz.partak
    V5_training_dataset/Track1_Headset/read_speech.tgz.partaj
    V5_training_dataset/Track1_Headset/read_speech.tgz.partai
    V5_training_dataset/Track1_Headset/read_speech.tgz.partah
    V5_training_dataset/Track1_Headset/read_speech.tgz.partag
    V5_training_dataset/Track1_Headset/read_speech.tgz.partaf
    V5_training_dataset/Track1_Headset/read_speech.tgz.partae
    V5_training_dataset/Track1_Headset/read_speech.tgz.partad
    V5_training_dataset/Track1_Headset/read_speech.tgz.partac
    V5_training_dataset/Track1_Headset/read_speech.tgz.partab
    V5_training_dataset/Track1_Headset/read_speech.tgz.partaa

    V5_training_dataset/Track1_Headset/italian_speech.tgz.partad
    V5_training_dataset/Track1_Headset/italian_speech.tgz.partac
    V5_training_dataset/Track1_Headset/italian_speech.tgz.partab
    V5_training_dataset/Track1_Headset/italian_speech.tgz.partaa

    V5_training_dataset/Track1_Headset/french_speech.tar.gz.partah
    V5_training_dataset/Track1_Headset/french_speech.tar.gz.partae
    V5_training_dataset/Track1_Headset/french_speech.tar.gz.partad
    V5_training_dataset/Track1_Headset/french_speech.tar.gz.partac
    V5_training_dataset/Track1_Headset/french_speech.tar.gz.partab
    V5_training_dataset/Track1_Headset/french_speech.tar.gz.partaa

    V5_training_dataset/Track1_Headset/emotional_speech.tgz


    V5_training_dataset/noise_fullband/datasets_fullband.noise_fullband.freesound_001.tar.bz2
    V5_training_dataset/noise_fullband/datasets_fullband.noise_fullband.freesound_000.tar.bz2

    V5_training_dataset/noise_fullband/datasets_fullband.noise_fullband.audioset_006.tar.bz2
    V5_training_dataset/noise_fullband/datasets_fullband.noise_fullband.audioset_005.tar.bz2
    V5_training_dataset/noise_fullband/datasets_fullband.noise_fullband.audioset_004.tar.bz2
    V5_training_dataset/noise_fullband/datasets_fullband.noise_fullband.audioset_003.tar.bz2
    V5_training_dataset/noise_fullband/datasets_fullband.noise_fullband.audioset_002.tar.bz2
    V5_training_dataset/noise_fullband/datasets_fullband.noise_fullband.audioset_001.tar.bz2
    V5_training_dataset/noise_fullband/datasets_fullband.noise_fullband.audioset_000.tar.bz2

    V5_training_dataset/datasets_fullband.impulse_responses_000.tar.bz2
)

###############################################################

AZURE_URL="https://dnschallengepublic.blob.core.windows.net/dns5archive"

OUTPUT_PATH="."

mkdir -p $OUTPUT_PATH/V5_training_dataset/noise_fullband
mkdir -p $OUTPUT_PATH/V5_training_dataset/Track1_Headset

for BLOB in ${BLOB_NAMES[@]}
do
    URL="$AZURE_URL/$BLOB"
    echo "Download: $BLOB"

    # DRY RUN: print HTTP response and Content-Length
    # WITHOUT downloading the files
    curl -s -I "$URL" | head -n 2

    # Actually download the files: UNCOMMENT when ready to download
    # curl "$URL" -o "$OUTPUT_PATH/$BLOB"
done

# 