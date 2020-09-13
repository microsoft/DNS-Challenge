# Noise Suppression Net 2 (NSNet2) baseline inference script

* As a baseline for ICASSP 2021 Deep Noise Suppression challenge, we will use the recently developed SE method based on Recurrent Neural Network (RNN). For ease of reference, we will call this method as Noise Suppression Net 2 (NSNet 2). 


## Prerequisites
- Python 3.0 and above
- pysoundfile (pip install pysoundfile)
- onnxruntime (pip install onnxruntime)

## Usage:
From the NSNet2-baseline directory, run run_nsnet2.py with the following required arguments:
- -i "Specify the path to noisy speech files that you want to enhance"
- -o "Specify the path to a directory where you want to store the enhanced clips"
- -m "Specify the path to the onnx model provided"

Use default values for the rest. Run to enhance the clips.
