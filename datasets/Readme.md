# Datasets for training
Datasets will be downloaded when you clone the repository. Run **git lfs install** for faster download.   
## Clean Speech
* The clean speech dataset is derived from the public audio books dataset called Librivox.
* Librivox has recordings of volunteers reading over 10,000 public domain audio books in various languages, with majority of which are in English. In total, there are 11,350 speakers.
* A section of these recordings is of excellent quality, meaning that the speech was recorded using good quality microphones in a silent and less reverberant environments.
* But there are many audio recordings that are of poor speech quality with speech distortion, background noise and reverberation. Hence, it is important to filter the data based on speech quality. 
* We used the online subjective test framework ITU-T P.808 to sort the book chapters by subjective quality.
* The audio chapters in Librivox are of variable length ranging from few seconds to several minutes.
* We sampled 10 random clips from each book chapter, each 10 seconds in duration. For each clip we had 3 ratings, and the Mean Opinion Score (MOS) across the all clips was used as the book chapter MOS.
* The upper quartile with respect to MOS was chosen as our clean speech dataset, which are top 25% of the clips with MOS as a metric.
* The upper quartile comprised of audio chapters with 4.3 ≤ MOS ≤ 5. We removed clips from speakers with less than 15 minutes of speech. The resulting dataset has 500 hours of speech from 2150 speakers. 
* All the filtered clips are then split into segments of 31 seconds.
* Singing voice is from VocalSet corpus. It has 10.1 hrs of singing from 20 professional singers.
* Emotion speech from diverse ethnic background is provided. Emotions such as Anger, Disgust, Fear, Happy, Neu-tral,  and  Sad  at  four  intensity  levels:  Low,  Medium, High, Unspecified are used.
* Non-English clips consisting of tonal and non-tonal languages are included.
* More details about the clean speech data can be found [here](https://github.com/microsoft/DNS-Challenge/blob/icassp21/addrir/docs/ICASSP_2021_deep_noise_suppression_challenge.pdf).

## Noise
* The noise clips were selected from Audioset and Freesound.
* Audioset is a collection of about 2 million human-labeled 10s sound clips drawn from YouTube videos and belong to about 600 audio events.
* Like the Librivox data, certain audio event classes are overrepresented. For example, there are over a million clips with audio classes music and speech and less than 200 clips for classes such as toothbrush, creak etc.
* Approximately, 42% of the clips have single class, but the rest may have 2 to 15 labels. 
* Hence, we developed a sampling approach to balance the dataset in such a way that each class has at least 500 clips.
* We also used a speech activity detector (trained classifier) to remove the clips with any kind of speech activity. The reason is to avoid suppression of speech by the noise suppression model trained to suppress speech like noise.
* The resulting dataset has about 150 audio classes and 60,000 clips. We also augmented an additional 10,000 noise clips downloaded from Freesound and DEMAND databases.
* The chosen noise types are more relevant to VOIP applications.

## Room Impulse Responses (RIR)
* 3076 real and about 115000 synthetic RIRs are provided.
* These room impulse responses can be convolved with clean speech to produce reverberant speech.
* Participants can simultaneously train for dereverb and denoising.

## Acoustic Parameters
* We provide two acoustic parameters:  (i) Reveberation time,T60 and (ii) Clarity, C50 for all audio clips in clean speechof  training  set. 
* These parameters are supposed to provide flex-ibility to researchers for choose a sub-set of provided data for controlled studies.

