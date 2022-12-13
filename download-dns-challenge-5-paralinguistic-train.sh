#!/usr/bin/bash

# ***** Dev Testset for 5th DNS Challenge at ICASSP 2023*****

# NOTE: Before downloading, make sure you have enough space
# on your local storage!

# Zip file is 181.8 MB. 
# -------------------------------------------------------------

URL="https://dnschallengepublic.blob.core.windows.net/dns5archive/V5_training_dataset/paralinguistic_training.zip"
echo "Download: $URL"
#
# DRY RUN: print HTTP header WITHOUT downloading the files
curl -s -I "$URL"
#
# Actually download the archive - UNCOMMENT it when ready to download
curl https://dnschallengepublic.blob.core.windows.net/dns5archive/V5_training_dataset/paralinguistic_training.zip --output 'paralinguistic_training.zip'
#wget --no-check-certificate "$URL"
