#!/usr/bin/bash

# ***** Datasets for ICASSP 2022 DNS Challenge 4 *****

# NOTE: Before downloading, make sure you have enough space
# on your local storage!

# In all, you will need at least 855GB to store the UNPACKED data.
# Archived, the same data takes 510GB total.

# Please comment out the files you don't need before launching
# the script.

# NOTE: By default, the script *DOES NOT* DOWNLOAD ANY FILES!
# Please scroll down and edit this script to pick the
# downloading method that works best for you.

# -------------------------------------------------------------
# The directory structure of the unpacked data is:

# . 855G
# +-- datasets 4.3G
# |   \-- impulse_responses 4.3G
# \-- datasets_fullband 850G
#     +-- emotional_speech 2.3G
#     +-- french_speech 63G
#     +-- german_speech 263G
#     +-- italian_speech 39G
#     +-- read_speech 300G
#     +-- russian_speech 12G
#     +-- spanish_speech 66G
#     +-- vctk_wav48_silence_trimmed 39G
#     +-- VocalSet_48kHz_mono 1G
#     +-- dev_testset 3G
#     |   +-- enrollment_data 644M
#     |   +-- noisy_testclips 2.4G
#     \-- noise_fullband 60G

BLOB_NAMES=(

    datasets_fullband/read_speech_000_0.00_3.72.tar.bz2
    datasets_fullband/read_speech_001_3.72_3.85.tar.bz2
    datasets_fullband/read_speech_002_3.85_3.93.tar.bz2
    datasets_fullband/read_speech_003_3.93_3.98.tar.bz2
    datasets_fullband/read_speech_004_3.98_4.02.tar.bz2
    datasets_fullband/read_speech_005_4.02_4.06.tar.bz2
    datasets_fullband/read_speech_006_4.06_4.09.tar.bz2
    datasets_fullband/read_speech_007_4.09_4.12.tar.bz2
    datasets_fullband/read_speech_008_4.12_4.15.tar.bz2
    datasets_fullband/read_speech_009_4.15_4.17.tar.bz2
    datasets_fullband/read_speech_010_4.17_4.19.tar.bz2
    datasets_fullband/read_speech_011_4.19_4.22.tar.bz2
    datasets_fullband/read_speech_012_4.22_4.24.tar.bz2
    datasets_fullband/read_speech_013_4.24_4.25.tar.bz2
    datasets_fullband/read_speech_014_4.25_4.27.tar.bz2
    datasets_fullband/read_speech_015_4.27_4.29.tar.bz2
    datasets_fullband/read_speech_016_4.29_4.31.tar.bz2
    datasets_fullband/read_speech_017_4.31_4.33.tar.bz2
    datasets_fullband/read_speech_018_4.33_4.35.tar.bz2
    datasets_fullband/read_speech_019_4.35_4.37.tar.bz2
    datasets_fullband/read_speech_020_4.37_4.39.tar.bz2
    datasets_fullband/read_speech_021_4.39_4.41.tar.bz2
    datasets_fullband/read_speech_022_4.41_4.43.tar.bz2
    datasets_fullband/read_speech_023_4.43_4.45.tar.bz2
    datasets_fullband/read_speech_024_4.45_4.48.tar.bz2
    datasets_fullband/read_speech_025_4.48_4.51.tar.bz2
    datasets_fullband/read_speech_026_4.51_4.54.tar.bz2
    datasets_fullband/read_speech_027_4.54_4.59.tar.bz2
    datasets_fullband/read_speech_028_4.59_4.71.tar.bz2
    datasets_fullband/read_speech_029_4.71_NA.tar.bz2
    datasets_fullband/read_speech_030_NA_NA.tar.bz2
    datasets_fullband/read_speech_031_NA_NA.tar.bz2
    datasets_fullband/read_speech_032_NA_NA.tar.bz2
    datasets_fullband/read_speech_033_NA_NA.tar.bz2
    datasets_fullband/read_speech_034_NA_NA.tar.bz2
    datasets_fullband/read_speech_035_NA_NA.tar.bz2
    datasets_fullband/read_speech_036_NA_NA.tar.bz2
    datasets_fullband/read_speech_037_NA_NA.tar.bz2
    datasets_fullband/read_speech_038_NA_NA.tar.bz2
    datasets_fullband/read_speech_039_NA_NA.tar.bz2
    datasets_fullband/read_speech_040_NA_NA.tar.bz2
    datasets_fullband/read_speech_041_NA_NA.tar.bz2
    datasets_fullband/read_speech_042_NA_NA.tar.bz2
    datasets_fullband/read_speech_043_NA_NA.tar.bz2
    datasets_fullband/read_speech_044_NA_NA.tar.bz2
    datasets_fullband/read_speech_045_NA_NA.tar.bz2
    datasets_fullband/read_speech_046_NA_NA.tar.bz2
    datasets_fullband/read_speech_047_NA_NA.tar.bz2
    datasets_fullband/read_speech_048_NA_NA.tar.bz2
    datasets_fullband/read_speech_049_NA_NA.tar.bz2
    datasets_fullband/read_speech_050_NA_NA.tar.bz2
    datasets_fullband/read_speech_051_NA_NA.tar.bz2
    datasets_fullband/read_speech_052_NA_NA.tar.bz2
    datasets_fullband/read_speech_053_NA_NA.tar.bz2
    datasets_fullband/read_speech_054_NA_NA.tar.bz2
    datasets_fullband/read_speech_055_NA_NA.tar.bz2
    datasets_fullband/read_speech_056_NA_NA.tar.bz2
    datasets_fullband/read_speech_057_NA_NA.tar.bz2
    datasets_fullband/read_speech_058_NA_NA.tar.bz2
    datasets_fullband/read_speech_059_NA_NA.tar.bz2
    datasets_fullband/read_speech_060_NA_NA.tar.bz2
    datasets_fullband/read_speech_061_NA_NA.tar.bz2
    datasets_fullband/read_speech_062_NA_NA.tar.bz2
    datasets_fullband/read_speech_063_NA_NA.tar.bz2
    datasets_fullband/read_speech_064_NA_NA.tar.bz2
    datasets_fullband/read_speech_065_NA_NA.tar.bz2
    datasets_fullband/read_speech_066_NA_NA.tar.bz2
    datasets_fullband/read_speech_067_NA_NA.tar.bz2
    datasets_fullband/read_speech_068_NA_NA.tar.bz2
    datasets_fullband/read_speech_069_NA_NA.tar.bz2
    datasets_fullband/read_speech_070_NA_NA.tar.bz2
    datasets_fullband/read_speech_071_NA_NA.tar.bz2
    datasets_fullband/read_speech_072_NA_NA.tar.bz2
    datasets_fullband/read_speech_073_NA_NA.tar.bz2
    datasets_fullband/read_speech_074_NA_NA.tar.bz2
    datasets_fullband/read_speech_075_NA_NA.tar.bz2
    datasets_fullband/read_speech_076_NA_NA.tar.bz2
    datasets_fullband/read_speech_077_NA_NA.tar.bz2
    datasets_fullband/read_speech_078_NA_NA.tar.bz2
    datasets_fullband/read_speech_079_NA_NA.tar.bz2
    datasets_fullband/read_speech_080_NA_NA.tar.bz2
    datasets_fullband/read_speech_081_NA_NA.tar.bz2
    datasets_fullband/read_speech_082_NA_NA.tar.bz2
    datasets_fullband/read_speech_083_NA_NA.tar.bz2
    datasets_fullband/read_speech_084_NA_NA.tar.bz2
    datasets_fullband/read_speech_085_NA_NA.tar.bz2
    datasets_fullband/read_speech_086_NA_NA.tar.bz2
    datasets_fullband/read_speech_087_NA_NA.tar.bz2
    datasets_fullband/read_speech_088_NA_NA.tar.bz2
    datasets_fullband/read_speech_089_NA_NA.tar.bz2
    datasets_fullband/read_speech_090_NA_NA.tar.bz2
    datasets_fullband/read_speech_091_NA_NA.tar.bz2
    datasets_fullband/read_speech_092_NA_NA.tar.bz2
    datasets_fullband/read_speech_093_NA_NA.tar.bz2
    datasets_fullband/read_speech_094_NA_NA.tar.bz2
    datasets_fullband/read_speech_095_NA_NA.tar.bz2
    datasets_fullband/read_speech_096_NA_NA.tar.bz2
    datasets_fullband/read_speech_097_NA_NA.tar.bz2
    datasets_fullband/read_speech_098_NA_NA.tar.bz2
    datasets_fullband/read_speech_099_NA_NA.tar.bz2
    datasets_fullband/read_speech_100_NA_NA.tar.bz2
    datasets_fullband/read_speech_101_NA_NA.tar.bz2
    datasets_fullband/read_speech_102_NA_NA.tar.bz2
    datasets_fullband/read_speech_103_NA_NA.tar.bz2
    datasets_fullband/read_speech_104_NA_NA.tar.bz2
    datasets_fullband/read_speech_105_NA_NA.tar.bz2
    datasets_fullband/read_speech_106_NA_NA.tar.bz2
    datasets_fullband/read_speech_107_NA_NA.tar.bz2
    datasets_fullband/read_speech_108_NA_NA.tar.bz2
    datasets_fullband/read_speech_109_NA_NA.tar.bz2
    datasets_fullband/read_speech_110_NA_NA.tar.bz2
    datasets_fullband/read_speech_111_NA_NA.tar.bz2
    datasets_fullband/read_speech_112_NA_NA.tar.bz2
    datasets_fullband/read_speech_113_NA_NA.tar.bz2
    datasets_fullband/read_speech_114_NA_NA.tar.bz2
    datasets_fullband/read_speech_115_NA_NA.tar.bz2
    datasets_fullband/read_speech_116_NA_NA.tar.bz2
    datasets_fullband/read_speech_117_NA_NA.tar.bz2
    datasets_fullband/read_speech_118_NA_NA.tar.bz2
    datasets_fullband/read_speech_119_NA_NA.tar.bz2
    datasets_fullband/read_speech_120_NA_NA.tar.bz2
    datasets_fullband/read_speech_121_NA_NA.tar.bz2
    datasets_fullband/read_speech_122_NA_NA.tar.bz2
    datasets_fullband/read_speech_123_NA_NA.tar.bz2
    datasets_fullband/read_speech_124_NA_NA.tar.bz2
    datasets_fullband/read_speech_125_NA_NA.tar.bz2
    datasets_fullband/read_speech_126_NA_NA.tar.bz2
    datasets_fullband/read_speech_127_NA_NA.tar.bz2
    datasets_fullband/read_speech_128_NA_NA.tar.bz2
    datasets_fullband/read_speech_129_NA_NA.tar.bz2
    datasets_fullband/read_speech_130_NA_NA.tar.bz2
    datasets_fullband/read_speech_131_NA_NA.tar.bz2
    datasets_fullband/read_speech_132_NA_NA.tar.bz2
    datasets_fullband/read_speech_133_NA_NA.tar.bz2
    datasets_fullband/read_speech_134_NA_NA.tar.bz2
    datasets_fullband/read_speech_135_NA_NA.tar.bz2
    datasets_fullband/read_speech_136_NA_NA.tar.bz2
    datasets_fullband/read_speech_137_NA_NA.tar.bz2
    datasets_fullband/read_speech_138_NA_NA.tar.bz2
    datasets_fullband/read_speech_139_NA_NA.tar.bz2
    datasets_fullband/read_speech_140_NA_NA.tar.bz2
    datasets_fullband/read_speech_141_NA_NA.tar.bz2
    datasets_fullband/read_speech_142_NA_NA.tar.bz2
    datasets_fullband/read_speech_143_NA_NA.tar.bz2
    datasets_fullband/read_speech_144_NA_NA.tar.bz2
    datasets_fullband/read_speech_145_NA_NA.tar.bz2
    datasets_fullband/read_speech_146_NA_NA.tar.bz2
    datasets_fullband/read_speech_147_NA_NA.tar.bz2
    datasets_fullband/read_speech_148_NA_NA.tar.bz2
    datasets_fullband/read_speech_149_NA_NA.tar.bz2
    datasets_fullband/read_speech_150_NA_NA.tar.bz2
    datasets_fullband/read_speech_151_NA_NA.tar.bz2
    datasets_fullband/read_speech_152_NA_NA.tar.bz2
    datasets_fullband/read_speech_153_NA_NA.tar.bz2
    datasets_fullband/read_speech_154_NA_NA.tar.bz2
    datasets_fullband/read_speech_155_NA_NA.tar.bz2
    datasets_fullband/read_speech_156_NA_NA.tar.bz2
    datasets_fullband/read_speech_157_NA_NA.tar.bz2
    datasets_fullband/read_speech_158_NA_NA.tar.bz2
    datasets_fullband/read_speech_159_NA_NA.tar.bz2

    datasets_fullband/french_speech_000_NA_NA.tar.bz2
    datasets_fullband/french_speech_001_NA_NA.tar.bz2
    datasets_fullband/french_speech_002_NA_NA.tar.bz2
    datasets_fullband/french_speech_003_NA_NA.tar.bz2
    datasets_fullband/french_speech_004_NA_NA.tar.bz2
    datasets_fullband/french_speech_005_NA_NA.tar.bz2
    datasets_fullband/french_speech_006_NA_NA.tar.bz2
    datasets_fullband/french_speech_007_NA_NA.tar.bz2
    datasets_fullband/french_speech_008_NA_NA.tar.bz2
    datasets_fullband/french_speech_009_NA_NA.tar.bz2
    datasets_fullband/french_speech_010_NA_NA.tar.bz2
    datasets_fullband/french_speech_011_NA_NA.tar.bz2
    datasets_fullband/french_speech_012_NA_NA.tar.bz2
    datasets_fullband/french_speech_013_NA_NA.tar.bz2
    datasets_fullband/french_speech_014_NA_NA.tar.bz2
    datasets_fullband/french_speech_015_NA_NA.tar.bz2
    datasets_fullband/french_speech_016_NA_NA.tar.bz2
    datasets_fullband/french_speech_017_NA_NA.tar.bz2
    datasets_fullband/french_speech_018_NA_NA.tar.bz2
    datasets_fullband/french_speech_019_NA_NA.tar.bz2
    datasets_fullband/french_speech_020_NA_NA.tar.bz2
    datasets_fullband/french_speech_021_NA_NA.tar.bz2
    datasets_fullband/french_speech_022_NA_NA.tar.bz2
    datasets_fullband/french_speech_023_NA_NA.tar.bz2
    datasets_fullband/french_speech_024_NA_NA.tar.bz2
    datasets_fullband/french_speech_025_NA_NA.tar.bz2
    datasets_fullband/french_speech_026_NA_NA.tar.bz2
    datasets_fullband/french_speech_027_NA_NA.tar.bz2
    datasets_fullband/french_speech_028_NA_NA.tar.bz2
    datasets_fullband/french_speech_029_NA_NA.tar.bz2
    datasets_fullband/french_speech_030_NA_NA.tar.bz2
    datasets_fullband/french_speech_031_NA_NA.tar.bz2
    datasets_fullband/french_speech_032_NA_NA.tar.bz2

    datasets_fullband/german_speech_000_0.00_3.56.tar.bz2
    datasets_fullband/german_speech_001_3.56_3.73.tar.bz2
    datasets_fullband/german_speech_002_3.73_3.84.tar.bz2
    datasets_fullband/german_speech_003_3.84_3.91.tar.bz2
    datasets_fullband/german_speech_004_3.91_3.98.tar.bz2
    datasets_fullband/german_speech_005_3.98_4.04.tar.bz2
    datasets_fullband/german_speech_006_4.04_4.10.tar.bz2
    datasets_fullband/german_speech_007_4.10_4.17.tar.bz2
    datasets_fullband/german_speech_008_4.17_4.25.tar.bz2
    datasets_fullband/german_speech_009_4.25_4.35.tar.bz2
    datasets_fullband/german_speech_010_4.35_NA.tar.bz2
    datasets_fullband/german_speech_011_NA_NA.tar.bz2
    datasets_fullband/german_speech_012_NA_NA.tar.bz2
    datasets_fullband/german_speech_013_NA_NA.tar.bz2
    datasets_fullband/german_speech_014_NA_NA.tar.bz2
    datasets_fullband/german_speech_015_NA_NA.tar.bz2
    datasets_fullband/german_speech_016_NA_NA.tar.bz2
    datasets_fullband/german_speech_017_NA_NA.tar.bz2
    datasets_fullband/german_speech_018_NA_NA.tar.bz2
    datasets_fullband/german_speech_019_NA_NA.tar.bz2
    datasets_fullband/german_speech_020_NA_NA.tar.bz2
    datasets_fullband/german_speech_021_NA_NA.tar.bz2
    datasets_fullband/german_speech_022_NA_NA.tar.bz2
    datasets_fullband/german_speech_023_NA_NA.tar.bz2
    datasets_fullband/german_speech_024_NA_NA.tar.bz2
    datasets_fullband/german_speech_025_NA_NA.tar.bz2
    datasets_fullband/german_speech_026_NA_NA.tar.bz2
    datasets_fullband/german_speech_027_NA_NA.tar.bz2
    datasets_fullband/german_speech_028_NA_NA.tar.bz2
    datasets_fullband/german_speech_029_NA_NA.tar.bz2
    datasets_fullband/german_speech_030_NA_NA.tar.bz2
    datasets_fullband/german_speech_031_NA_NA.tar.bz2
    datasets_fullband/german_speech_032_NA_NA.tar.bz2
    datasets_fullband/german_speech_033_NA_NA.tar.bz2
    datasets_fullband/german_speech_034_NA_NA.tar.bz2
    datasets_fullband/german_speech_035_NA_NA.tar.bz2
    datasets_fullband/german_speech_036_NA_NA.tar.bz2
    datasets_fullband/german_speech_037_NA_NA.tar.bz2
    datasets_fullband/german_speech_038_NA_NA.tar.bz2
    datasets_fullband/german_speech_039_NA_NA.tar.bz2
    datasets_fullband/german_speech_040_NA_NA.tar.bz2
    datasets_fullband/german_speech_041_NA_NA.tar.bz2
    datasets_fullband/german_speech_042_NA_NA.tar.bz2
    datasets_fullband/german_speech_043_NA_NA.tar.bz2
    datasets_fullband/german_speech_044_NA_NA.tar.bz2
    datasets_fullband/german_speech_045_NA_NA.tar.bz2
    datasets_fullband/german_speech_046_NA_NA.tar.bz2
    datasets_fullband/german_speech_047_NA_NA.tar.bz2
    datasets_fullband/german_speech_048_NA_NA.tar.bz2
    datasets_fullband/german_speech_049_NA_NA.tar.bz2
    datasets_fullband/german_speech_050_NA_NA.tar.bz2
    datasets_fullband/german_speech_051_NA_NA.tar.bz2
    datasets_fullband/german_speech_052_NA_NA.tar.bz2
    datasets_fullband/german_speech_053_NA_NA.tar.bz2
    datasets_fullband/german_speech_054_NA_NA.tar.bz2
    datasets_fullband/german_speech_055_NA_NA.tar.bz2
    datasets_fullband/german_speech_056_NA_NA.tar.bz2
    datasets_fullband/german_speech_057_NA_NA.tar.bz2
    datasets_fullband/german_speech_058_NA_NA.tar.bz2
    datasets_fullband/german_speech_059_NA_NA.tar.bz2
    datasets_fullband/german_speech_060_NA_NA.tar.bz2
    datasets_fullband/german_speech_061_NA_NA.tar.bz2
    datasets_fullband/german_speech_062_NA_NA.tar.bz2
    datasets_fullband/german_speech_063_NA_NA.tar.bz2
    datasets_fullband/german_speech_064_NA_NA.tar.bz2
    datasets_fullband/german_speech_065_NA_NA.tar.bz2
    datasets_fullband/german_speech_066_NA_NA.tar.bz2
    datasets_fullband/german_speech_067_NA_NA.tar.bz2
    datasets_fullband/german_speech_068_NA_NA.tar.bz2
    datasets_fullband/german_speech_069_NA_NA.tar.bz2
    datasets_fullband/german_speech_070_NA_NA.tar.bz2
    datasets_fullband/german_speech_071_NA_NA.tar.bz2
    datasets_fullband/german_speech_072_NA_NA.tar.bz2
    datasets_fullband/german_speech_073_NA_NA.tar.bz2
    datasets_fullband/german_speech_074_NA_NA.tar.bz2
    datasets_fullband/german_speech_075_NA_NA.tar.bz2
    datasets_fullband/german_speech_076_NA_NA.tar.bz2
    datasets_fullband/german_speech_077_NA_NA.tar.bz2
    datasets_fullband/german_speech_078_NA_NA.tar.bz2
    datasets_fullband/german_speech_079_NA_NA.tar.bz2
    datasets_fullband/german_speech_080_NA_NA.tar.bz2
    datasets_fullband/german_speech_081_NA_NA.tar.bz2
    datasets_fullband/german_speech_082_NA_NA.tar.bz2
    datasets_fullband/german_speech_083_NA_NA.tar.bz2
    datasets_fullband/german_speech_084_NA_NA.tar.bz2
    datasets_fullband/german_speech_085_NA_NA.tar.bz2
    datasets_fullband/german_speech_086_NA_NA.tar.bz2
    datasets_fullband/german_speech_087_NA_NA.tar.bz2
    datasets_fullband/german_speech_088_NA_NA.tar.bz2
    datasets_fullband/german_speech_089_NA_NA.tar.bz2
    datasets_fullband/german_speech_090_NA_NA.tar.bz2
    datasets_fullband/german_speech_091_NA_NA.tar.bz2
    datasets_fullband/german_speech_092_NA_NA.tar.bz2
    datasets_fullband/german_speech_093_NA_NA.tar.bz2
    datasets_fullband/german_speech_094_NA_NA.tar.bz2
    datasets_fullband/german_speech_095_NA_NA.tar.bz2
    datasets_fullband/german_speech_096_NA_NA.tar.bz2
    datasets_fullband/german_speech_097_NA_NA.tar.bz2
    datasets_fullband/german_speech_098_NA_NA.tar.bz2
    datasets_fullband/german_speech_099_NA_NA.tar.bz2
    datasets_fullband/german_speech_100_NA_NA.tar.bz2
    datasets_fullband/german_speech_101_NA_NA.tar.bz2
    datasets_fullband/german_speech_102_NA_NA.tar.bz2
    datasets_fullband/german_speech_103_NA_NA.tar.bz2
    datasets_fullband/german_speech_104_NA_NA.tar.bz2
    datasets_fullband/german_speech_105_NA_NA.tar.bz2
    datasets_fullband/german_speech_106_NA_NA.tar.bz2
    datasets_fullband/german_speech_107_NA_NA.tar.bz2
    datasets_fullband/german_speech_108_NA_NA.tar.bz2
    datasets_fullband/german_speech_109_NA_NA.tar.bz2
    datasets_fullband/german_speech_110_NA_NA.tar.bz2
    datasets_fullband/german_speech_111_NA_NA.tar.bz2
    datasets_fullband/german_speech_112_NA_NA.tar.bz2
    datasets_fullband/german_speech_113_NA_NA.tar.bz2
    datasets_fullband/german_speech_114_NA_NA.tar.bz2
    datasets_fullband/german_speech_115_NA_NA.tar.bz2
    datasets_fullband/german_speech_116_NA_NA.tar.bz2
    datasets_fullband/german_speech_117_NA_NA.tar.bz2
    datasets_fullband/german_speech_118_NA_NA.tar.bz2
    datasets_fullband/german_speech_119_NA_NA.tar.bz2
    datasets_fullband/german_speech_120_NA_NA.tar.bz2
    datasets_fullband/german_speech_121_NA_NA.tar.bz2
    datasets_fullband/german_speech_122_NA_NA.tar.bz2
    datasets_fullband/german_speech_123_NA_NA.tar.bz2
    datasets_fullband/german_speech_124_NA_NA.tar.bz2
    datasets_fullband/german_speech_125_NA_NA.tar.bz2
    datasets_fullband/german_speech_126_NA_NA.tar.bz2
    datasets_fullband/german_speech_127_NA_NA.tar.bz2
    datasets_fullband/german_speech_128_NA_NA.tar.bz2
    datasets_fullband/german_speech_129_NA_NA.tar.bz2
    datasets_fullband/german_speech_130_NA_NA.tar.bz2
    datasets_fullband/german_speech_131_NA_NA.tar.bz2
    datasets_fullband/german_speech_132_NA_NA.tar.bz2
    datasets_fullband/german_speech_133_NA_NA.tar.bz2
    datasets_fullband/german_speech_134_NA_NA.tar.bz2
    datasets_fullband/german_speech_135_NA_NA.tar.bz2
    datasets_fullband/german_speech_136_NA_NA.tar.bz2
    datasets_fullband/german_speech_137_NA_NA.tar.bz2
    datasets_fullband/german_speech_138_NA_NA.tar.bz2
    datasets_fullband/german_speech_139_NA_NA.tar.bz2
    datasets_fullband/german_speech_140_NA_NA.tar.bz2

    datasets_fullband/italian_speech_000_0.00_3.97.tar.bz2
    datasets_fullband/italian_speech_001_3.97_4.19.tar.bz2
    datasets_fullband/italian_speech_002_4.19_4.36.tar.bz2
    datasets_fullband/italian_speech_003_4.36_4.64.tar.bz2
    datasets_fullband/italian_speech_004_4.64_NA.tar.bz2
    datasets_fullband/italian_speech_005_NA_NA.tar.bz2
    datasets_fullband/italian_speech_006_NA_NA.tar.bz2
    datasets_fullband/italian_speech_007_NA_NA.tar.bz2
    datasets_fullband/italian_speech_008_NA_NA.tar.bz2
    datasets_fullband/italian_speech_009_NA_NA.tar.bz2
    datasets_fullband/italian_speech_010_NA_NA.tar.bz2
    datasets_fullband/italian_speech_011_NA_NA.tar.bz2
    datasets_fullband/italian_speech_012_NA_NA.tar.bz2
    datasets_fullband/italian_speech_013_NA_NA.tar.bz2
    datasets_fullband/italian_speech_014_NA_NA.tar.bz2
    datasets_fullband/italian_speech_015_NA_NA.tar.bz2
    datasets_fullband/italian_speech_016_NA_NA.tar.bz2
    datasets_fullband/italian_speech_017_NA_NA.tar.bz2
    datasets_fullband/italian_speech_018_NA_NA.tar.bz2
    datasets_fullband/italian_speech_019_NA_NA.tar.bz2
    datasets_fullband/italian_speech_020_NA_NA.tar.bz2

    datasets_fullband/russian_speech_000_0.00_4.26.tar.bz2
    datasets_fullband/russian_speech_001_4.26_NA.tar.bz2
    datasets_fullband/russian_speech_002_NA_NA.tar.bz2
    datasets_fullband/russian_speech_003_NA_NA.tar.bz2
    datasets_fullband/russian_speech_004_NA_NA.tar.bz2
    datasets_fullband/russian_speech_005_NA_NA.tar.bz2
    datasets_fullband/russian_speech_006_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_000_0.00_4.02.tar.bz2

    datasets_fullband/spanish_speech_001_4.02_4.37.tar.bz2
    datasets_fullband/spanish_speech_002_4.37_NA.tar.bz2
    datasets_fullband/spanish_speech_003_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_004_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_005_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_006_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_007_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_008_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_009_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_010_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_011_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_012_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_013_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_014_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_015_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_016_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_017_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_018_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_019_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_020_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_021_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_022_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_023_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_024_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_025_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_026_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_027_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_028_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_029_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_030_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_031_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_032_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_033_NA_NA.tar.bz2
    datasets_fullband/spanish_speech_034_NA_NA.tar.bz2

    datasets_fullband/vctk_wav48_silence_trimmed_000_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_001_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_002_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_003_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_004_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_005_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_006_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_007_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_008_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_009_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_010_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_011_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_012_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_013_NA_NA.tar.bz2
    datasets_fullband/vctk_wav48_silence_trimmed_014_NA_NA.tar.bz2

    datasets_fullband/VocalSet_48kHz_mono.tar.bz2

    datasets_fullband/emotional_speech.tar.bz2

    datasets.impulse_responses.tar.bz2

    datasets_fullband.dev_testset.enrollment_data.tar.bz2
    datasets_fullband.dev_testset.noisy_testclips.tar.bz2

    datasets_fullband.noise_fullband.tar.bz2
)

###############################################################

AZURE_URL="https://dns4public.blob.core.windows.net/dns4archive"

OUTPUT_PATH="."

mkdir -p $OUTPUT_PATH/{datasets,datasets_fullband}

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
    # curl "$URL" | tar -C "$OUTPUT_PATH" fjxv -
done
