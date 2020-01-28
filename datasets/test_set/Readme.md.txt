# Initial Testset for DNS Challenge

## Real Recordings
* The real recordings comprise of hand picked and validated samples from audioset and recorded noisy clips collected internally at Microsoft.
* The real recordings collected internally at Microsoft consist of recorded noisy speech in various open office and conference rooms noisy conditions.
* The real recordings are more representative to what is observed in the wild.

## Synthetic Test Set
* **synthetic** directory has 2 sub directories **no_reverb** and **with_reverb**
* For synthetic test clips, we used Graz University’s clean speech dataset, which consists of 4,270 recorded sentences spoken by 20 speakers.
* The noise clips for testing are sampled from audioset and freesound and these are not present in the training set.
* For the synthetic clips with reverb, we add reverberation to the clean files using the room impulse responses recorded internally at Microsoft with RT60 ranging from 300ms to 1300ms.
* Synthetic clips come with ground truth references, so that objective metrics such as PESQ and POLQA can be used to evaluate the method.


