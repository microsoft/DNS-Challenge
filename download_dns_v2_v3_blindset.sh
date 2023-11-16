#!/usr/bin/bash

# ***** BLIND Testset for 2nd and 3rd DNS Challenges combined with additional handpicked clips*****

# NOTE: Before downloading, make sure you have enough space
# on your local storage!

# -------------------------------------------------------------
# The directory structure of the unpacked data is:

#
# +-- V2_V3_Challenge_Combined_Blindset
# |   +-- handpicked_emotion_testclips_16k_600_withSNR ---> (600 emotional clips)
# |   +-- mouseclicks_testclips_withSNR_16k            ---> (100 mouseclicks clips)
# |   +-- noisy_blind_testset_v2_challenge_withSNR_16k ---> (700 blindset clips from V2 challenge)
# |   +-- noisy_blind_testset_v3_challenge_withSNR_16k ---> (600 blindset clips from V3 challenge)

URL="https://dnschallengepublic.blob.core.windows.net/dns3archive/V2_V3_Challenge_Combined_Blindset.zip"

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
