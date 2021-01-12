High quality data to match the existing low quality DNS data was extracted from the AudioMP3 directory of the original dataset. The AudioMP3 was chosen over the FLV as the files seemed very similar (with the FLV using an MP3 track at the same bitrate for sound). Even though the wav files have been resampled to 38 kHz, signal content only exists till around 11 kHz suggesting an original sampling frequency of ~22.5 kHz.

# Two files with issues:
1. 1040_ITH_SAD_X.wav is misnamed in the low quality DNS-Challenge (and low quality AudioWAV folder) - instead of 1040_ITH_SAD_XX.wav as in the VidoFLV and AudioMP3 folders of the original dataset and here
2. The high quality 1047_IEO_SAD_LO.wav does not match with the low quality 1047_IEO_SAD_LO.wav because of an issue with the file in the original dataset. Neither the flv nor the mp3 files were helpful in that matter - all the high quality files contain 3 different emotions while the LQ file is the right one (sad)
