# DNSMOS: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors

Human subjective evaluation is the ”gold standard” to evaluate speech quality optimized for human perception.  Perceptual objective metrics serve as a proxy for subjective scores. The conventional and widely used metrics require a reference clean speech signal, which is unavailable in real recordings. The no-reference approaches correlate poorly with human ratings and are not widely adopted in the research community. One of the biggest use cases of these perceptual objective metrics is to evaluate noise suppression algorithms. DNSMOS generalizes well in challenging test conditions with a high correlation to human ratings in stack ranking noise suppression methods. More details can be found in [DNSMOS paper](https://arxiv.org/pdf/2010.15258.pdf).

## Evaluation methodology:
Use the **dnsmos_local.py** script.
1. To compute a personalized MOS score (where interfering speaker is penalized) provide the '-p' argument
Ex: python dnsmos_local.py -t C:\temp\SampleClips -o sample.csv -p
2. To compute a regular MOS score omit the '-p' argument.
Ex: python dnsmos_local.py -t C:\temp\SampleClips -o sample.csv

## Citation:
If you have used the API for your research and development purpose, please cite the [DNSMOS paper](https://arxiv.org/pdf/2010.15258.pdf):
```BibTex
@inproceedings{reddy2021dnsmos,
  title={Dnsmos: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors},
  author={Reddy, Chandan KA and Gopal, Vishak and Cutler, Ross},
  booktitle={ICASSP 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  pages={6493--6497},
  year={2021},
  organization={IEEE}
}
```

If you used DNSMOS P.835 please cite the [DNSMOS P.835](https://arxiv.org/pdf/2110.01763.pdf) paper:
  
```BibTex
@inproceedings{reddy2022dnsmos,
  title={DNSMOS P.835: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors},
  author={Reddy, Chandan KA and Gopal, Vishak and Cutler, Ross},
  booktitle={ICASSP 2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  year={2022},
  organization={IEEE}
}
 ```
