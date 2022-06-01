# Speech To Text

Project to combine VAD, Speaker Diarization, Speech Recognition together.



## Getting Started

As DeepSpeech pre-trained English model is too big to commit to git. You could download from 
(https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3)

Please put the downloaded model files into folder **speech-to-text/deepspeech/models**

```shell
# Create and activate a virtual environment
python3 -m venv speech-to-text/env
source speech-to-text/env/bin/activate

# Install prerequisites
pip3 install -r requirements.txt

# Speech To Text
python3 speech_to_text.py --audio=wavs/test2.wav
```

It will output the txt file with speakers and speech text, side by side the wav file 

## Overview

It's just to combine speaker diarization and speech recognization together. 

Only support 16k sample rate PCM wav file. You can use ffmpeg to convert sound file format. i.e.
```
ffmpeg -i input.mp3 -acodec pcm_s16le -ar 16000 output.wav
```
**Main flows**
1. Filter out silence frames and break down to segments with webrtcvad.

2. Generate utterances spec with librosa

3. Get utterances features with ghostvlad

4. Classify features with uisrnn model

5. Recognize speeches segment by segment with deepspeech

*It might takes long period(tens minutes) if the wav is too big.(seems uisrnn part takes the longest)
The test wavs in the wavs folder are from movie sound clips. The speech accuracy is not perfect, it might relative to the pretrained deepspeech model and the background noise*

### Prerequisites

- pytorch
- keras
- tensorflow
- pyaudio
- librosa
- webrtcvad
- deepspeech


## References

- [DeepSpeech](https://github.com/mozilla/DeepSpeech)
- [Speaker-Diarization](https://github.com/taylorlu/Speaker-Diarization)
- [uis-rnn](https://github.com/google/uis-rnn)
- [py-webrtcvad](https://github.com/wiseman/py-webrtcvad)
- [librosa](https://github.com/librosa/librosa)
- [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis)
- [kaldi](https://github.com/kaldi-asr/kaldi)
- [terry-yip](https://github.com/terry-yip)

### Tip

Following are the libs version installed in my env, just for your reference.

absl-py                      0.15.0
appdirs                      1.4.4
astunparse                   1.6.3
audioread                    2.1.9
cachetools                   5.0.0
certifi                      2021.10.8
cffi                         1.15.0
charset-normalizer           2.0.12
clang                        5.0
decorator                    5.1.1
deepspeech                   0.9.3
deepspeech-gpu               0.9.3
deepspeech-tflite            0.9.3
flatbuffers                  1.12
gast                         0.4.0
google-auth                  2.6.6
google-auth-oauthlib         0.4.6
google-pasta                 0.2.0
grpcio                       1.34.1
h5py                         3.1.0
idna                         3.3
importlib-metadata           4.11.3
joblib                       1.1.0
keras                        2.5.0rc0
keras-nightly                2.5.0.dev2021032900
Keras-Preprocessing          1.1.2
libclang                     14.0.1
librosa                      0.9.1
llvmlite                     0.33.0
Markdown                     3.3.7
numba                        0.50.1
numpy                        1.17.3
oauthlib                     3.2.0
opt-einsum                   3.3.0
packaging                    21.3
pip                          22.1
pooch                        1.6.0
protobuf                     3.20.1
pyasn1                       0.4.8
pyasn1-modules               0.2.8
pycparser                    2.21
pyparsing                    3.0.8
PyYAML                       6.0
requests                     2.27.1
requests-oauthlib            1.3.1
resampy                      0.2.2
rsa                          4.8
scikit-learn                 1.0.2
scipy                        1.8.0
setuptools                   56.0.0
six                          1.15.0
SoundFile                    0.10.3.post1
tensorboard                  2.8.0
tensorboard-data-server      0.6.1
tensorboard-plugin-wit       1.8.1
tensorflow                   2.5.0
tensorflow-estimator         2.5.0
tensorflow-gpu               2.5.0
tensorflow-io-gcs-filesystem 0.25.0
termcolor                    1.1.0
tf-estimator-nightly         2.8.0.dev2021122109
threadpoolctl                3.1.0
torch                        1.11.0
typing-extensions            3.7.4.3
urllib3                      1.26.9
vosk                         0.3.32
webrtcvad                    2.0.10
Werkzeug                     2.1.2
wheel                        0.37.1
wrapt                        1.12.1
zipp                         3.8.0
