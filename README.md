# ICASSP 2023 Deep Noise Suppression Challenge
Website: https://aka.ms/dns-challenge
Git Repo: https://github.com/microsoft/DNS-Challenge
Challenge Paper: <TBD> 

## Important features of this challenge
1. Along with noise suppression, it includes de-reverberation and suppression of interfering talkers for headset and speakerphone scenarios.
2. The challenge has two tracks: (i) Headset (wired/wireless headphone, earbuds such as airpods etc.) speech enhancement; (ii) Non-headset (speakerphone, built-in mic in laptop/desktop/mobile phone/other meeting devices etc.) speech enhancement. 
3. This challenge adopts the ITU-T P.835 subjective test framework to measure speech quality (SIG), background noise quality (BAK), and overall audio quality (OVRL). We modified the ITU-T P.835 to make it reliable for test clips with interfering (undesired neighboring) talkers. Along with P.835 scores, Word Accuracy (WAcc) is used to measure the performance of models.
4. Please NOTE that the intellectual property (IP) is not transferred to the challenge organizers, i.e., if code is shared/submitted, the participants remain the owners of their code (when the code is made publicly available, an appropriate license should be added).
5. There are new requirements for model related latency. Please check all requirements listed at https://www.microsoft.com/en-us/research/academic-program/deep-noise-suppression-challenge-icassp-2023/

## Baseline Speaker Embeddings
This challenge adopted pretrained ECAPA-TDNN model available in SpeechBrain as baseline speaker embeddings models, available at https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb. Participants can use any other publically available speaker embeddings model or develop their own speaker embedding extractor. Participants are encourage to explore RawNet3 models available at https://github.com/jungjee/RawNet

Previous DNS Challenge used RawNet2 speaker embeddings. So far, impact of different speaker embeddings for personalized speech enhancements is not studied in sufficient depth. 

# Install SpeechBrain with below command:
pip install speechbrain

#Compute Speaker Embeddings for your wav file with below command:

import torchaudio
from speechbrain.pretrained import EncoderClassifier
classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")
signal, fs =torchaudio.load('tests/samples/ASR/spk1_snt1.wav')
embeddings = classifier.encode_batch(signal)

## In this repository

This repository contains the datasets and scripts required for 5th DNS Challenge at ICASSP 2023, aka DNS
Challenge 5, or simply **DNS5**. For more details about the challenge, please see our
[website](https://www.microsoft.com/en-us/research/academic-program/deep-noise-suppression-challenge-icassp-2023/) and [paper](docs/ICASSP2023_5th_DNS_Challenge.pdf). For more details on the testing framework, please visit [P.835](https://github.com/microsoft/P.808).

## Details

* The **datasets_fullband** folder is a placeholder for the datasets. That is, our data downloader
  script by default will place the downloaded audio data there. After the download, it will contain
  clean speech, noise, and room impulse responses required for creating the training data.
  
* The **Baseline** directory contains the enhanced clips from dev testset for both tracks. 

* **download-dns-challenge-5-headset-training.sh** - this is the script to download the data for headset (Track 1). By default, the data will be placed into the `./datasets_fullband/` folder. Please take a look at the script and **uncomment** the perferred download method._ Unmodified, the script performs a dry run and retrieves only the HTTP headers for each archive.

* **download-dns-challenge-5-speakerphone-training.sh** - this is the script to download the data for speakerphone (Track 2).

* **noisyspeech_synthesizer_singleprocess.py** - is used to synthesize noisy-clean speech pairs for
  training purposes.

* **noisyspeech_synthesizer.cfg** - is the configuration file used to synthesize the data. Users are
required to accurately specify different parameters and provide the right paths to the datasets required to synthesize noisy speech.

* **audiolib.py** - contains modules required to synthesize datasets.
* **utils.py** - contains some utility functions required to synthesize the data.
* **unit_tests_synthesizer.py** - contains the unit tests to ensure sanity of the data.
* **requirements.txt** - contains all the libraries required for synthesizing the data.

## Datasets
**V5_dev_testset**: directory containing dev testsets for both tracks. Each testclip has 10s duration and the corresponding enrollment clips with 30s duration. 

**BLIND testset**: <TBD>

## WAcc script
https://github.com/microsoft/DNS-Challenge/tree/master/WAcc

## Wacc ground-truth transcript
Dev testset: available only for speakerphone track, see v5_dev_testset directory. For headset track, we are providing ASR output and list of prompts read during recording of testclips. Participants can help in correcting ASR output to generate the ground-truth transcripts.
Blind testset: <TBD>

### Data info

The default directory structure and the sizes of the datasets of the 5th DNS
Challenge are:

```
datasets_fullband 
+-- dev_testset 
+-- impulse_responses 5.9G
+-- noise_fullband 58G
\-- clean_fullband 827G
    +-- emotional_speech 2.4G
    +-- french_speech 62G
    +-- german_speech 319G
    +-- italian_speech 42G
    +-- read_speech 299G
    +-- russian_speech 12G
    +-- spanish_speech 65G
    +-- vctk_wav48_silence_trimmed 27G
    \-- VocalSet_48kHz_mono 974M
```

In all, you will need about 1TB to store the _unpacked_ data. Archived, the same data takes about
550GB total.

### Headset DNS track
### Data checksums

A CSV file containing file sizes and SHA1 checksums for audio clips in both Real-time *and*
Personalized DNS datasets is available at:
[dns5-datasets-files-sha1.csv.bz2](https://dns4public.blob.core.windows.net/dns4archive/dns5-datasets-files-sha1.csv.bz2).
The archive is 41.3MB in size and can be read in Python like this:
```python
import pandas as pd

sha1sums = pd.read_csv("dns5-datasets-files-sha1.csv.bz2", names=["size", "sha1", "path"])
```

## Code prerequisites
- Python 3.6 and above
- Python libraries: soundfile, librosa

**NOTE:** git LFS is *no longer required* for DNS Challenge. Please use the
`download-dns-challenge-5*.sh` scripts in this repo to download the data.

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
@inproceedings{dubey2023icassp,
  title={ICASSP 2023 Deep Noise Suppression Challenge},
  author={
 Dubey, Harishchandra and Aazami, Ashkan and Gopal, Vishak and Naderi, Babak and Braun, Sebastian and  Cutler, Ross and Gamper, Hannes and Golestaneh, Mehrsa and Aichner, Robert},
  booktitle={ICASSP},
  year={2023}
}
```

The previous challenges were: 
```BibTex
@inproceedings{dubey2022icassp,
  title={ICASSP 2022 Deep Noise Suppression Challenge},
  author={Dubey, Harishchandra and Gopal, Vishak and Cutler, Ross and Matusevych, Sergiy and Braun, Sebastian and Eskimez, Emre Sefik and Thakker, Manthan and Yoshioka, Takuya and Gamper, Hannes and Aichner, Robert},
  booktitle={ICASSP},
  year={2022}
}

@inproceedings{reddy2021interspeech,
  title={INTERSPEECH 2021 Deep Noise Suppression Challenge},
  author={Reddy, Chandan KA and Dubey, Harishchandra and Koishida, Kazuhito and Nair, Arun and Gopal, Vishak and Cutler, Ross and Braun, Sebastian and Gamper, Hannes and Aichner, Robert and Srinivasan, Sriram},
  booktitle={INTERSPEECH},
  year={2021}
}
```
```BibTex
@inproceedings{reddy2021icassp,
  title={ICASSP 2021 deep noise suppression challenge},
  author={Reddy, Chandan KA and Dubey, Harishchandra and Gopal, Vishak and Cutler, Ross and Braun, Sebastian and Gamper, Hannes and Aichner, Robert and Srinivasan, Sriram},
  booktitle={ICASSP},
  year={2021},
}
```
```BibTex
@inproceedings{reddy2020interspeech,
  title={The INTERSPEECH 2020 deep noise suppression challenge: Datasets, subjective testing framework, and challenge results},
  author={Reddy, Chandan KA and Gopal, Vishak and Cutler, Ross and Beyrami, Ebrahim and Cheng, Roger and Dubey, Harishchandra and Matusevych, Sergiy and Aichner, Robert and Aazami, Ashkan and Braun, Sebastian and others},
  booktitle={INTERSPEECH},
  year={2020}
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
@inproceedings{reddy2021dnsmos,
  title={DNSMOS: A Non-Intrusive Perceptual Objective Speech Quality metric to evaluate Noise Suppressors},
  author={Reddy, Chandan KA and Gopal, Vishak and Cutler, Ross},
  booktitle={ICASSP},
  year={2021}
}
```

```BibTex
@inproceedings{reddy2022dnsmos,
  title={DNSMOS P.835: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors},
  author={Reddy, Chandan KA and Gopal, Vishak and Cutler, Ross},
  booktitle={ICASSP},
  year={2022}
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
