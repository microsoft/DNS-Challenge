# Noise Suppression Net (NSNet) baseline inference script

* As a baseline for Interspeech 2020 Deep Noise Suppression challenge, we will use the recently developed SE method based on Recurrent Neural Network (RNN). For ease of reference, we will call this method as Noise Suppression Net (NSNet). The details about this method can be found in the [published paper](https://arxiv.org/pdf/2001.10601.pdf)
* This method uses log power spectra as input to predict the enhancement gain per frame using a learning machine based on Gated Recurrent Units (GRU) and fully connected layers. Please refer to the paper for more details of the method.
* NSNet is computationally efficient. It only takes 0.16ms to enhance a 20ms frame on an Intel quad core i5 machine using the ONNX run time v1.1 .

## Prerequisites
- Python 3.0 and above
- pysoundfile (pip install pysoundfile)
- onnxruntime (pip install onnxruntime)

## Files:
- nsnet_eval_local.py - Main script that calls onnx.py
- onnx.py - Frame based inference
- audiolib.py - Required audio libraries for inference
- nsnet-baseline-dnschallenge.onnx - Trained NSNet ONNX model used for inference

## Usage:
From the NSNet-baseline directory, run nsnet_eval_local.py with the following required arguments:
- --noisyspeechdir "Specify the path to noisy speech files that you want to enhance"
- --enhanceddir "Specify the path to a directory where you want to store the enhanced clips"
- --modelpath "Specify the path to the onnx model provided"

Use default values for the rest. Run to enhance the clips.

## Citation:
The baseline NSNet noise suppression:<br />  
@misc{xia2020weighted,<br />
    title={Weighted Speech Distortion Losses for Neural-network-based Real-time Speech Enhancement},<br />
    author={Yangyang Xia and Sebastian Braun and Chandan K. A. Reddy and Harishchandra Dubey and Ross Cutler and Ivan Tashev},<br />
    year={2020},<br />
    eprint={2001.10601},<br />
    archivePrefix={arXiv},<br />
    primaryClass={eess.AS}<br />
}
