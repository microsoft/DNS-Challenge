# DNSMOS: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors

Human subjective evaluation is the ”gold standard” to evaluate speech quality optimized for human perception.  Perceptual objective metrics serve as a proxy for subjective scores. The conventional and widely used metrics require a reference clean speech signal, which is unavailable in real recordings. The no-reference approaches correlate poorly with human ratings and are not widely adopted in the research community. One of the biggest use cases of these perceptual objective metrics is to evaluate noise suppression algorithms. DNSMOS generalizes well in challenging test conditions with a high correlation to human ratings in stack ranking noise suppression methods. More details can be found in [DNSMOS paper](https://arxiv.org/pdf/2010.15258.pdf).

## Evaluation methodology:
We have created a web-API for you to evaluate your audio clips.

For access to the API, please complete the following form: https://forms.office.com/r/pRhyZ0mQy3

We will send you the **AUTH_KEY** that you can insert in the **dnsmos.py** script.

Example command for P.835 evaluation of test clips: python dnsmos --testset_dir <test clips directory> --method p835

## Citation:
If you have used the API for your research and development purpose, please cite the DNSMOS paper
```BibTex
@article{reddy2020dnsmos,
  title={DNSMOS: A Non-Intrusive Perceptual Objective Speech Quality metric to evaluate Noise Suppressors},
  author={Reddy, Chandan KA and Gopal, Vishak and Cutler, Ross},
  journal={arXiv e-prints},
  pages={arXiv--2010},
  year={2020}
}
```

