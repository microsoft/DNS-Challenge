# INTERSPEECH 2021: 3rd Deep Noise Suppression (DNS) Challenge

This repository contains the datasets and scripts required for the 3rd DNS challenge. For more details about the challenge, please visit https://www.microsoft.com/en-us/research/dns-challenge/home. For more details on the testing framework, please visit [P.808](https://github.com/microsoft/P.808).

## Repo details:
* The **datasets** directory contains the clean speech, noise and room impulse responses for creating training data. It also contains the test set that participants can use during the development stages. We have fullband (48kHz) and wideband (16kHz) training data and testset. 

* The **NSNet2-baseline** directory contains the inference scripts and the ONNX model for the baseline Speech Enhancement method. 
* **noisyspeech_synthesizer_singleprocess.py** - is used to synthesize noisy-clean speech pairs for training purposes.
* **noisyspeech_synthesizer.cfg** - is the configuration file used to synthesize the data. Users are required to accurately specify different parameters and provide the right paths to the datasets required to synthesize noisy speech.
* **audiolib.py** - contains modules required to synthesize datasets.
* **utils.py** - contains some utility functions required to synthesize the data.
* **unit_tests_synthesizer.py** - contains the unit tests to ensure sanity of the data.
* **requirements.txt** - contains all the libraries required for synthesizing the data.

## Prerequisites
- Python 3.0 and above
- Soundfile (pip install pysoundfile), librosa

## Usage:
1. Install librosa 
```
pip install librosa
```
2. Install Git Large File Storage for faster download of the datasets.
```
git lfs install
git lfs track "*.wav"
git add .gitattributes
```
3. Clone the repository. 
```
git clone https://github.com/microsoft/DNS-Challenge DNS-Challenge
```
4. Edit **noisyspeech_synthesizer.cfg** to specify the required parameters described in the file and include the paths to clean speech, noise and impulse response related csv files. Also, specify the paths to the destination directories and store the logs.
5. Create dataset 
```
python noisyspeech_synthesizer_singleprocess.py
```

## Citation:
For the datasets and the DNS challenge:<br />  

```BibTex
@article{reddy2020icassp,
  title={ICASSP 2021 Deep Noise Suppression Challenge},
  author={Reddy, Chandan KA and Dubey, Harishchandra and Gopal, Vishak and Cutler, Ross and Braun, Sebastian and Gamper, Hannes and Aichner, Robert and Srinivasan, Sriram},
  journal={arXiv preprint arXiv:2009.06122},
  year={2020}
}
```

The baseline NSNet noise suppression:<br />  
```BibTex
@INPROCEEDINGS{9054254, 
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

The P.808 test framework:<br />
```BibTex
@article{naderi2020open,
  title={An Open source Implementation of ITU-T Recommendation P. 808 with Validation},
  author={Naderi, Babak and Cutler, Ross},
  journal={arXiv preprint arXiv:2005.08138},
  year={2020}
}
```

DNSMOS API: <br />
```BibTex
@article{reddy2020dnsmos,
  title={DNSMOS: A Non-Intrusive Perceptual Objective Speech Quality metric to evaluate Noise Suppressors},
  author={Reddy, Chandan KA and Gopal, Vishak and Cutler, Ross},
  journal={arXiv e-prints},
  pages={arXiv--2010},
  year={2020}
}
```

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

# Legal Notices

Microsoft and any contributors grant you a license to the Microsoft documentation and other content
in this repository under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/legalcode),
see the [LICENSE](LICENSE) file, and grant you a license to any code in the repository under the [MIT License](https://opensource.org/licenses/MIT), see the
[LICENSE-CODE](LICENSE-CODE) file.

Microsoft, Windows, Microsoft Azure and/or other Microsoft products and services referenced in the documentation
may be either trademarks or registered trademarks of Microsoft in the United States and/or other countries.
The licenses for this project do not grant you rights to use any Microsoft names, logos, or trademarks.
Microsoft's general trademark guidelines can be found at http://go.microsoft.com/fwlink/?LinkID=254653.

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
