#!/usr/bin/bash

# ***** 5th DNS Challenge at ICASSP 2023*****
# Track 1 Headset Clean speech: All Languages 
# -------------------------------------------------------------
# In all, you will need about 1TB to store the UNPACKED data.
# Archived, the same data takes about 550GB total.

# Please comment out the files you don't need before launching
# the script.

# NOTE: By default, the script *DOES NOT* DOWNLOAD ANY FILES!
# Please scroll down and edit this script to pick the
# downloading method that works best for you.

# -------------------------------------------------------------
# The directory structure of the unpacked data is:

# datasets_fullband 
# \-- clean_fullband 827G
#     +-- emotional_speech 2.4G
#     +-- french_speech 62G
#     +-- german_speech 319G
#     +-- italian_speech 42G
#     +-- read_speech 299G
#     +-- russian_speech 12G
#     +-- spanish_speech 65G
#     +-- vctk_wav48_silence_trimmed 27G
#     \-- VocalSet_48kHz_mono 974M

BLOB_NAMES=(

    Track1_Headset/VocalSet_48kHz_mono.tgz
    Track1_Headset/emotional_speech.tgz

    Track1_Headset/french_speech.tar.gz.partaa
    Track1_Headset/french_speech.tar.gz.partab
    Track1_Headset/french_speech.tar.gz.partac
    Track1_Headset/french_speech.tar.gz.partad
    Track1_Headset/french_speech.tar.gz.partae
    Track1_Headset/french_speech.tar.gz.partah

    Track1_Headset/german_speech.tgz.partaa
    Track1_Headset/german_speech.tgz.partab
    Track1_Headset/german_speech.tgz.partac
    Track1_Headset/german_speech.tgz.partad
    Track1_Headset/german_speech.tgz.partae
    Track1_Headset/german_speech.tgz.partaf
    Track1_Headset/german_speech.tgz.partag
    Track1_Headset/german_speech.tgz.partah
    Track1_Headset/german_speech.tgz.partaj
    Track1_Headset/german_speech.tgz.partal
    Track1_Headset/german_speech.tgz.partam
    Track1_Headset/german_speech.tgz.partan
    Track1_Headset/german_speech.tgz.partao
    Track1_Headset/german_speech.tgz.partap
    Track1_Headset/german_speech.tgz.partaq
    Track1_Headset/german_speech.tgz.partar
    Track1_Headset/german_speech.tgz.partas
    Track1_Headset/german_speech.tgz.partat
    Track1_Headset/german_speech.tgz.partau
    Track1_Headset/german_speech.tgz.partav
    Track1_Headset/german_speech.tgz.partaw

    Track1_Headset/italian_speech.tgz.partaa
    Track1_Headset/italian_speech.tgz.partab
    Track1_Headset/italian_speech.tgz.partac
    Track1_Headset/italian_speech.tgz.partad
    
    Track1_Headset/read_speech.tgz.partaa
    Track1_Headset/read_speech.tgz.partab
    Track1_Headset/read_speech.tgz.partac
    Track1_Headset/read_speech.tgz.partad
    Track1_Headset/read_speech.tgz.partae
    Track1_Headset/read_speech.tgz.partaf
    Track1_Headset/read_speech.tgz.partag
    Track1_Headset/read_speech.tgz.partah
    Track1_Headset/read_speech.tgz.partai
    Track1_Headset/read_speech.tgz.partaj
    Track1_Headset/read_speech.tgz.partak
    Track1_Headset/read_speech.tgz.partal
    Track1_Headset/read_speech.tgz.partam
    Track1_Headset/read_speech.tgz.partan
    Track1_Headset/read_speech.tgz.partao
    Track1_Headset/read_speech.tgz.partap
    Track1_Headset/read_speech.tgz.partaq
    Track1_Headset/read_speech.tgz.partar
    Track1_Headset/read_speech.tgz.partas
    Track1_Headset/read_speech.tgz.partat
    Track1_Headset/read_speech.tgz.partau

    Track1_Headset/russian_speech.tgz

    Track1_Headset/spanish_speech.tgz.partaa
    Track1_Headset/spanish_speech.tgz.partab
    Track1_Headset/spanish_speech.tgz.partac
    Track1_Headset/spanish_speech.tgz.partad
    Track1_Headset/spanish_speech.tgz.partae
    Track1_Headset/spanish_speech.tgz.partaf
    Track1_Headset/spanish_speech.tgz.partag

    Track1_Headset/vctk_wav48_silence_trimmed.tgz.partaa
    Track1_Headset/vctk_wav48_silence_trimmed.tgz.partab
    Track1_Headset/vctk_wav48_silence_trimmed.tgz.partac
)

###############################################################
# this data is extracted from datasets used in Track 2.

AZURE_URL="https://dnschallengepublic.blob.core.windows.net/dns5archive/V5_training_dataset"

OUTPUT_PATH="./datasets_fullband"

mkdir -p $OUTPUT_PATH/{clean_fullband}

for BLOB in ${BLOB_NAMES[@]}
do
    URL="$AZURE_URL/$BLOB"
    echo "Download: $BLOB"

    # DRY RUN: print HTTP response and Content-Length
    # WITHOUT downloading the files
    curl -s -I "$URL" | head -n 2

    # Actually download the files: UNCOMMENT when ready to download
    # curl "$URL" -o "$OUTPUT_PATH/$BLOB"

    # Same as above, but using wget
    # wget "$URL" -O "$OUTPUT_PATH/$BLOB"

    # Same, + unpack files on the fly
    # curl "$URL" | tar -C "$OUTPUT_PATH" -f - -x -j
done
