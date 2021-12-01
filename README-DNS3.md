
# Deep Noise Suppression (DNS) Challenge 3 - INTERSPEECH 2021

**NOTE:** This README describes the **PAST** DNS Challenge!

The data for it is still available, and is described below. If you are interested in the latest DNS
Challenge, please refer to the main [README.md](README.md) file.

## In this repository

This repository contains the datasets and scripts required for INTERSPEECH 2021 DNS Challenge, AKA
DNS Challenge 3, or DNS3. For more details about the challenge, please see our
[paper](https://arxiv.org/pdf/2101.01902.pdf) and the challenge
[website](https://www.microsoft.com/en-us/research/academic-program/deep-noise-suppression-challenge-interspeech-2021/).
For more details on the testing framework, please visit [P.835](https://github.com/microsoft/P.808).

## Details

* The **datasets** directory is a placeholder for the wideband datasets. That is, our data
  downloader script by default will place the downloader audio data here. After the download, this
  directory will contain clean speech, noise, and room impulse responses required for creating the
  training data for wideband scenario. The script will also download here the test set that
  participants can use during the development stages.
* The **datasets_fullband** directory is a placeholder for the fullband audio data. The downloader
  script will download here the datasets that contain clean speech and noise audio clips required
  for creating training data for fullband scenario.
* The **NSNet2-baseline** directory contains the inference scripts and the ONNX model for the
  baseline Speech Enhancement method for wideband. 
* **download-dns-challenge-3.sh** - this is the script to download the data. By default, the data
  will be placed into `datasets/` and `datasets_fullband/` directories. Please take a look at the
  script and uncomment the perferred download method. Unmodified, the script performs a dry
  run and retrieves only the HTTP headers for each archive.
* **noisyspeech_synthesizer_singleprocess.py** - is used to synthesize noisy-clean speech pairs for
  training purposes.
* **noisyspeech_synthesizer.cfg** - is the configuration file used to synthesize the data. Users are
  required to accurately specify different parameters and provide the right paths to the datasets
  required to synthesize noisy speech.
* **audiolib.py** - contains modules required to synthesize datasets.
* **utils.py** - contains some utility functions required to synthesize the data.
* **unit_tests_synthesizer.py** - contains the unit tests to ensure sanity of the data.
* **requirements.txt** - contains all the libraries required for synthesizing the data.

## Datasets

The default directory structure and the sizes of the datasets available for DNS Challenge are:

```
datasets 229G
├── clean 204G
│   ├── emotional_speech 403M
│   ├── french_data 21G
│   ├── german_speech 66G
│   ├── italian_speech 14G
│   ├── mandarin_speech 21G
│   ├── read_speech 61G
│   ├── russian_speech 5.1G
│   ├── singing_voice 979M
│   └── spanish_speech 17G
├── dev_testset 211M
├── impulse_responses 4.3G
│   ├── SLR26 2.1G
│   └── SLR28 2.3G
└── noise 20G
```

And, for the fullband data,
```
datasets_fullband 600G
├── clean_fullband 542G
│   ├── VocalSet_48kHz_mono 974M
│   ├── emotional_speech 1.2G
│   ├── french_data 62G
│   ├── german_speech 194G
│   ├── italian_speech 42G
│   ├── read_speech 182G
│   ├── russian_speech 12G
│   └── spanish_speech 50G
├── dev_testset_fullband 630M
└── noise_fullband 58G
```

## Code prerequisites
- Python 3.6 and above
- Python libraries: soundfile, librosa

**NOTE:** git LFS is *no longer required* for DNS Challenge. Please use the
`download-dns-challenge-3.sh` script in this repo to download the data.

## Usage:

1. Install Python libraries
```bash
pip3 install soundfile librosa
```
2. Clone the repository. 
```bash
git clone https://github.com/microsoft/DNS-Challenge
```

3. Edit **noisyspeech_synthesizer.cfg** to specify the required parameters described in the file and
   include the paths to clean speech, noise and impulse response related csv files. Also, specify
   the paths to the destination directories and store the logs.

4. Create dataset 
```bash
python3 noisyspeech_synthesizer_singleprocess.py
```

## Citation:
If you use this dataset in a publication please cite the following paper:<br />  

```BibTex
@inproceedings{reddy2021interspeech,
  title={INTERSPEECH 2021 Deep Noise Suppression Challenge},
  author={Reddy, Chandan KA and Dubey, Harishchandra and Koishida, Kazuhito and Nair, Arun and Gopal, Vishak and Cutler, Ross and Braun, Sebastian and Gamper, Hannes and Aichner, Robert and Srinivasan, Sriram},
  booktitle={INTERSPEECH},
  year={2021}
}
```

The baseline NSNet noise suppression:<br />  
```BibTex
@inproceedings{9054254, 
    author={Y. {Xia} and S. {Braun} and C. K. A. {Reddy} and H. {Dubey} and R. {Cutler} and I. {Tashev}}, 
    booktitle={ICASSP 2020 - 2020 IEEE International Conference on Acoustics, 
    Speech and Signal Processing (ICASSP)}, 
    title={Weighted Speech Distortion Losses for Neural-Network-Based Real-Time Speech Enhancement}, 
    year={2020}, volume={}, number={}, pages={871-875},}
```

```BibTex
@misc{braun2020data,
    title={Data augmentation and loss normalization for deep noise suppression},
    author={Sebastian Braun and Ivan Tashev},
    year={2020},
    eprint={2008.06412},
    archivePrefix={arXiv},
    primaryClass={eess.AS}
}
```

The P.835 test framework:<br />
```BibTex
@inproceedings{naderi2021crowdsourcing,
  title={Subjective Evaluation of Noise Suppression Algorithms in Crowdsourcing},
  author={Naderi, Babak and Cutler, Ross},
  booktitle={INTERSPEECH},
  year={2021}
}
```

DNSMOS API: <br />
```BibTex
@inproceedings{reddy2020dnsmos,
  title={DNSMOS: A Non-Intrusive Perceptual Objective Speech Quality metric to evaluate Noise Suppressors},
  author={Reddy, Chandan KA and Gopal, Vishak and Cutler, Ross},
  booktitle={ICASSP},
  year={2020}
}
```

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide a
CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

# Legal Notices

Microsoft and any contributors grant you a license to the Microsoft documentation and other content
in this repository under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/legalcode),
see the [LICENSE](LICENSE) file, and grant you a license to any code in the repository under the [MIT License](https://opensource.org/licenses/MIT), see the
[LICENSE-CODE](LICENSE-CODE) file.

Microsoft, Windows, Microsoft Azure and/or other Microsoft products and services referenced in the
documentation may be either trademarks or registered trademarks of Microsoft in the United States
and/or other countries. The licenses for this project do not grant you rights to use any Microsoft
names, logos, or trademarks. Microsoft's general trademark guidelines can be found at
http://go.microsoft.com/fwlink/?LinkID=254653.

Privacy information can be found at https://privacy.microsoft.com/en-us/

Microsoft and any contributors reserve all other rights, whether under their respective copyrights, patents,
or trademarks, whether by implication, estoppel or otherwise.


## Dataset licenses
MICROSOFT PROVIDES THE DATASETS ON AN "AS IS" BASIS. MICROSOFT MAKES NO WARRANTIES, EXPRESS OR IMPLIED, GUARANTEES OR CONDITIONS WITH RESPECT TO YOUR USE OF THE DATASETS. TO THE EXTENT PERMITTED UNDER YOUR LOCAL LAW, MICROSOFT DISCLAIMS ALL LIABILITY FOR ANY DAMAGES OR LOSSES, INLCUDING DIRECT, CONSEQUENTIAL, SPECIAL, INDIRECT, INCIDENTAL OR PUNITIVE, RESULTING FROM YOUR USE OF THE DATASETS.

The datasets are provided under the original terms that Microsoft received such datasets. See below for more information about each dataset.

The datasets used in this project are licensed as follows:
1. Clean speech: 
* https://librivox.org/; License: https://librivox.org/pages/public-domain/
* PTDB-TUG: Pitch Tracking Database from Graz University of Technology https://www.spsc.tugraz.at/databases-and-tools/ptdb-tug-pitch-tracking-database-from-graz-university-of-technology.html; License: http://opendatacommons.org/licenses/odbl/1.0/ 
* Edinburgh 56 speaker dataset: https://datashare.is.ed.ac.uk/handle/10283/2791; License: https://datashare.is.ed.ac.uk/bitstream/handle/10283/2791/license_text?sequence=11&isAllowed=y 
* VocalSet: A Singing Voice Dataset https://zenodo.org/record/1193957#.X1hkxYtlCHs; License: Creative Commons Attribution 4.0 International
* Emotion data corpus: CREMA-D (Crowd-sourced Emotional Multimodal Actors Dataset)
https://github.com/CheyneyComputerScience/CREMA-D; License: http://opendatacommons.org/licenses/dbcl/1.0/
* The VoxCeleb2 Dataset http://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox2.html; License: http://www.robots.ox.ac.uk/~vgg/data/voxceleb/
The VoxCeleb dataset is available to download for commercial/research purposes under a Creative Commons Attribution 4.0 International License. The copyright remains with the original owners of the video. A complete version of the license can be found here. 
* VCTK Dataset: https://homepages.inf.ed.ac.uk/jyamagis/page3/page58/page58.html; License: This corpus is licensed under Open Data Commons Attribution License (ODC-By) v1.0.
http://opendatacommons.org/licenses/by/1.0/ 

2. Noise:
* Audioset: https://research.google.com/audioset/index.html; License: https://creativecommons.org/licenses/by/4.0/
* Freesound: https://freesound.org/ Only files with CC0 licenses were selected; License: https://creativecommons.org/publicdomain/zero/1.0/
* Demand: https://zenodo.org/record/1227121#.XRKKxYhKiUk; License: https://creativecommons.org/licenses/by-sa/3.0/deed.en_CA

3. RIR datasets: OpenSLR26 and OpenSLR28:
* http://www.openslr.org/26/
* http://www.openslr.org/28/
* License: Apache 2.0

## Code license
MIT License

Copyright (c) Microsoft Corporation.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
