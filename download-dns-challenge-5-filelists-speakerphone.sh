#!/usr/bin/bash

# ***** Dev Testset for 5th DNS Challenge at ICASSP 2023*****

# NOTE: Before downloading, make sure you have enough space
# on your local storage!

# Zip file is 1.5MB. 
# It contains speaker ID filsists for speakerphone training clean speech (Track 2)
# -------------------------------------------------------------

URL="https://dnschallengepublic.blob.core.windows.net/dns5archive/filelists_speakerphone.zip"
echo "Download: $URL"
#
# DRY RUN: print HTTP header WITHOUT downloading the files
curl -s -I "$URL"
#
# Actually download the archive - UNCOMMENT it when ready to download
curl https://dnschallengepublic.blob.core.windows.net/dns5archive/filelists_speakerphone.zip --output 'filelists_speakerphone.zip'
#wget --no-check-certificate "$URL"
