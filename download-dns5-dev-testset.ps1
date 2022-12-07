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

$AZURE_URL="https://dns4public.blob.core.windows.net/dns4archive"

$OUTPUT_PATH="."

URL="https://dnschallengepublic.blob.core.windows.net/dns5archive/V5_dev_testset.zip"

Write-Output "Download: $URL"

# DRY RUN: print HTTP response and Content-Length
# WITHOUT downloading the files
curl -s -I "$URL" | head -n 2

# Actually download the files: UNCOMMENT when ready to download
# curl "$URL" -o "$OUTPUT_PATH/$BLOB"

# Same as above, but using wget
# wget "$URL" -O "$OUTPUT_PATH/$BLOB"

# Same, + unpack files on the fly
# curl "$URL" | tar -C "$OUTPUT_PATH" -f - -x -j