#!/usr/bin/bash

# ***** Datasets for ICASSP 2022 DNS Challenge 4 - Personalized DNS Track *****

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
# The directory structure of the unpacked data is:

# . 362G
# +-- datasets_fullband 64G
# |   +-- impulse_responses 5.9G
# |   \-- noise_fullband 58G
# +-- pdns_training_set 294G
# |   +-- enrollment_embeddings 115M
# |   +-- enrollment_wav 42G
# |   +-- raw/clean 252G
# |       +-- english 168G
# |       +-- french 2.1G
# |       +-- german 53G
# |       +-- italian 17G
# |       +-- russian 6.8G
# |       \-- spanish 5.4G
# \-- personalized_dev_testset 3.3G

BLOB_NAMES=(

    pdns_training_set/raw/pdns_training_set.raw.clean.english_000.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_001.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_002.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_003.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_004.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_005.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_006.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_007.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_008.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_009.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_010.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_011.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_012.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_013.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_014.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_015.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_016.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_017.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_018.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_019.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.english_020.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.french_000.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.german_000.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.german_001.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.german_002.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.german_003.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.german_004.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.german_005.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.german_006.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.german_007.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.german_008.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.italian_000.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.italian_001.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.italian_002.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.russian_000.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.spanish_000.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.spanish_001.tar.bz2
    pdns_training_set/raw/pdns_training_set.raw.clean.spanish_002.tar.bz2

    pdns_training_set/enrollment_wav/pdns_training_set.enrollment_wav.english_000.tar.bz2
    pdns_training_set/enrollment_wav/pdns_training_set.enrollment_wav.english_001.tar.bz2
    pdns_training_set/enrollment_wav/pdns_training_set.enrollment_wav.english_002.tar.bz2
    pdns_training_set/enrollment_wav/pdns_training_set.enrollment_wav.english_003.tar.bz2
    pdns_training_set/enrollment_wav/pdns_training_set.enrollment_wav.english_004.tar.bz2
    pdns_training_set/enrollment_wav/pdns_training_set.enrollment_wav.french_000.tar.bz2
    pdns_training_set/enrollment_wav/pdns_training_set.enrollment_wav.german_000.tar.bz2
    pdns_training_set/enrollment_wav/pdns_training_set.enrollment_wav.german_001.tar.bz2
    pdns_training_set/enrollment_wav/pdns_training_set.enrollment_wav.italian_000.tar.bz2
    pdns_training_set/enrollment_wav/pdns_training_set.enrollment_wav.russian_000.tar.bz2
    pdns_training_set/enrollment_wav/pdns_training_set.enrollment_wav.spanish_000.tar.bz2

    pdns_training_set/pdns_training_set.enrollment_embeddings_000.tar.bz2

    datasets_fullband/noise_fullband/datasets_fullband.noise_fullband.audioset_000.tar.bz2
    datasets_fullband/noise_fullband/datasets_fullband.noise_fullband.audioset_001.tar.bz2
    datasets_fullband/noise_fullband/datasets_fullband.noise_fullband.audioset_002.tar.bz2
    datasets_fullband/noise_fullband/datasets_fullband.noise_fullband.audioset_003.tar.bz2
    datasets_fullband/noise_fullband/datasets_fullband.noise_fullband.audioset_004.tar.bz2
    datasets_fullband/noise_fullband/datasets_fullband.noise_fullband.audioset_005.tar.bz2
    datasets_fullband/noise_fullband/datasets_fullband.noise_fullband.audioset_006.tar.bz2

    datasets_fullband/noise_fullband/datasets_fullband.noise_fullband.freesound_000.tar.bz2
    datasets_fullband/noise_fullband/datasets_fullband.noise_fullband.freesound_001.tar.bz2

    datasets_fullband/datasets_fullband.impulse_responses_000.tar.bz2

    personalized_dev_testset/personalized_dev_testset.enrollment.tar.bz2
    personalized_dev_testset/personalized_dev_testset.noisy_testclips.tar.bz2
)

###############################################################

AZURE_URL="https://dns4public.blob.core.windows.net/dns4archive"

OUTPUT_PATH="."

mkdir -p $OUTPUT_PATH/{pdns_training_set/{raw,enrollment_wav},datasets_fullband/noise_fullband}

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
