#!/usr/bin/bash

# ***** Dev Testset for 5th DNS Challenge at ICASSP 2023*****

# NOTE: Before downloading, make sure you have enough space
# on your local storage!

# Zip file is 2.9 GB. Unzipped data is 4GB.

# -------------------------------------------------------------
# The directory structure of the unpacked data is:

#
# +-- V5_dev_testset 64G
# |   +-- Track1_Headset ---> (enrol, noisy)
# |   +-- Track2_Speakerphone ---> (enrol, noisy)

URL="https://dnschallengepublic.blob.core.windows.net/dns5archive/V5_dev_testset.zip"
echo "Download: $URL"
#
# DRY RUN: print HTTP header WITHOUT downloading the files
curl -s -I "$URL"
#
# Actually download the archive - UNCOMMENT it when ready to download
#do
wget "$URL"

#done
# curl "$URL" -o "$BLOB"
# Same as above, but using wget
#wget "$URL 
# Same, + unpack files on the fly
# curl "$URL" | tar -f - -x -j
