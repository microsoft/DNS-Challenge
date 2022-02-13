#!/usr/bin/bash

# ***** Datasets for INTERSPEECH 2020 DNS Challenge 1 *****

# NOTE: This data is for the *PAST* challenge!
# Current DNS Challenge is ICASSP 2022 DNS Challenge 4, which
# has its own download script, `download-dns-challenge-4.sh`

###############################################################

AZURE_URL="https://dns3public.blob.core.windows.net/dns3archive"

mkdir -p ./datasets/

URL="$AZURE_URL/datasets-interspeech2020.tar.bz2"
echo "Download: $BLOB"

# DRY RUN: print HTTP header WITHOUT downloading the files
curl -s -I "$URL"

# Actually download the archive - UNCOMMENT it when ready to download
# curl "$URL" -o "$BLOB"

# Same as above, but using wget
# wget "$URL" -O "$BLOB"

# Same, + unpack files on the fly
# curl "$URL" | tar -f - -x -j
