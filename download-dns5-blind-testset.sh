#!/usr/bin/bash

# ***** BLIND Testset for 5th DNS Challenge at ICASSP 2023*****

# NOTE: Before downloading, make sure you have enough space
# on your local storage!

# -------------------------------------------------------------
# The directory structure of the unpacked data is:

#
# +-- V5_BlindTestSet
# |   +-- Track1_Headset ---> (enrol, noisy)
# |   +-- Track2_Speakerphone ---> (enrol, noisy)

URL="https://dnschallengepublic.blob.core.windows.net/dns5archive/V5_BlindTestSet.zip"

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
