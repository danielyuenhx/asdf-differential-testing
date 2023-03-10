# CrossASR

Code for ICSME 2020 "CrossASR: Efficient Differential Testing of Automatic Speech Recognition via Text-To-Speech" by [Muhammad Hilmi Asyrofi](https://www.linkedin.com/in/mhilmiasyrofi/), [Ferdian Thung](https://scholar.google.com/citations?hl=en&user=47okQ-UAAAAJ), [David Lo](https://scholar.google.com/citations?user=Ra4bt-oAAAAJ&hl=en), and [Lingxiao Jiang](https://scholar.google.com/citations?hl=en&user=0hssXLPZL2YC)

[Paper PDF](https://mhilmiasyrofi.github.io/papers/CrossASR.pdf) | [DOI](https://ieeexplore.ieee.org/document/9240600)

### Overview

Automatic speech recognition (ASR) systems are ubiquitous parts of modern life. It can be found in our smartphones, desktops, and smart home systems. To ensure its correctness in recognizing speeches, ASR needs to be tested. Testing ASR requires test cases in the form of audio files and their transcribed texts. Building these test cases manually, however, is tedious and time-consuming.

To deal with the aforementioned challenge, in this work, we propose CrossASR, an approach that capitalizes the existing Text-To-Speech (TTS) systems to automatically generate test cases for ASR systems. CrossASR is a differential testing solution that compares outputs of multiple ASR systems to uncover erroneous behaviors among ASRs. CrossASR efficiently generates test cases to uncover failures with as few generated tests as possible; it does so by employing a failure probability predictor to pick the texts with the highest likelihood of leading to failed test cases. As a black-box approach, CrossASR can generate test cases for any ASR, including when the ASR model is not available (e.g., when evaluating the reliability of various third-party ASR services).


We evaluated the performance of CrossASR on 20,000 English texts (i.e., sentences) in the [Europarl corpus](https://www.statmt.org/europarl/). We use 4 TTSes (i.e., [Google](https://cloud.google.com/text-to-speech), [ResponsiveVoice](https://responsivevoice.org/), [Festival](http://www.cstr.ed.ac.uk/projects/festival/), and [Espeak](http://espeak.sourceforge.net/)) and 4 ASRs (i.e., [Deepspeech](https://github.com/mozilla/DeepSpeech), [Deepspeech2](https://github.com/PaddlePaddle/DeepSpeech), [wav2letter++](https://github.com/facebookresearch/wav2letter), and [wit](https://wit.ai/)). We use more than one TTS to avoid bias that comes from a particular TTS.




## Prepare Virtual Environment


### 1. Install the Python development environment on your system

```
sudo apt update
sudo apt install python3-dev python3-pip python3-venv
```

### 2. Create a virtual environment

Create a new virtual environment by choosing a Python interpreter and making a ./env directory to hold it:

```
python3 -m venv --system-site-packages ~/./env
```

Activate the virtual environment using a shell-specific command:

```
source ~/./env/bin/activate  # sh, bash, or zsh
```


## TTSes

### 1. Google

We use [gTTS](https://pypi.org/project/gTTS/) (Google Text-to-Speech), a Python library and CLI tool to interface with Google Translate text-to-speech API.

```
pip install gTTS
```

#### Trial
```
if [ ! -d "audio/" ]
then 
    mkdir audio
fi

mkdir audio/google/
gtts-cli 'hello world google' --output audio/google/hello.mp3
ffmpeg -i audio/google/hello.mp3  -acodec pcm_s16le -ac 1 -ar 16000 audio/google/hello.wav -y
```

### 2. ResponsiveVoice

We use [rvTTS](https://pypi.org/project/rvtts/), a cli tool for converting text to mp3 files using ResponsiveVoice's API.

```
pip install rvtts
```

#### Trial
```
mkdir audio/rv/
rvtts --voice english_us_male --text "hello responsive voice trial" -o audio/rv/hello.mp3
ffmpeg -i audio/rv/hello.mp3  -acodec pcm_s16le -ac 1 -ar 16000 audio/rv/hello.wav -y
```

### 3. Festival

[Festival](http://www.cstr.ed.ac.uk/projects/festival/) is a free TTS written in C++. It is developed by The Centre for Speech Technology Research at the University of Edinburgh. Festival are distributed under an X11-type licence allowing unrestricted commercial and non-commercial use alike. Festival is a command-line program that already installed on Ubuntu 16.04

#### Trial
```
sudo apt install festival
mkdir audio/festival/
festival -b "(utt.save.wave (SayText \"hello festival \") \"audio/festival/hello.wav\" 'riff)"
```

### 4. Espeak

[eSpeak](http://espeak.sourceforge.net/) is a compact open source software speech synthesizer for English and other languages.

```
sudo apt install espeak

mkdir audio/espeak/
espeak "hello e speak" --stdout > audio/espeak/hello.wav
ffmpeg -i audio/espeak/hello.wav  -acodec pcm_s16le -ac 1 -ar 16000 audio/espeak/hello.wav -y
```


## ASRs

### 1. Deepspeech

[DeepSpeech](https://github.com/mozilla/DeepSpeech) is an open source Speech-To-Text engine, using a model trained by machine learning techniques based on [Baidu's Deep Speech research paper](https://arxiv.org/abs/1412.5567). **CrossASR uses [Deepspeech-0.6.1](https://github.com/mozilla/DeepSpeech/tree/v0.6.1)**

```
pip install deepspeech===0.6.1

if [ ! -d "models/" ]
then 
    mkdir models
fi

cd models
mkdir deepspeech
cd deepspeech 
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.6.1/deepspeech-0.6.1-models.tar.gz
tar xvf deepspeech-0.6.1-models.tar.gz
cd ../../
```

Please follow [this link for more detailed installation](https://github.com/mozilla/DeepSpeech/tree/v0.6.1).

#### Trial
```
deepspeech --model models/deepspeech/deepspeech-0.6.1-models/output_graph.pbmm --lm models/deepspeech/deepspeech-0.6.1-models/lm.binary --trie models/deepspeech/deepspeech-0.6.1-models/trie --audio audio/google/hello.wav
```

### 2. Deepspeech2

[DeepSpeech2](https://github.com/PaddlePaddle/DeepSpeech) is an open-source implementation of end-to-end Automatic Speech Recognition (ASR) engine, based on [Baidu's Deep Speech 2 paper](http://proceedings.mlr.press/v48/amodei16.pdf), with [PaddlePaddle](https://github.com/PaddlePaddle/Paddle) platform.

#### Setup a docker container for Deepspeech2

[Original Source](https://github.com/PaddlePaddle/DeepSpeech#running-in-docker-container)

```
cd models/
git clone https://github.com/PaddlePaddle/DeepSpeech.git
cp deepspeech2-api.py DeepSpeech/
cd DeepSpeech/models/librispeech/
sh download_model.sh
cd ../../../../
cd models/DeepSpeech/models/lm
sh download_lm_en.sh
cd ../../../../
docker pull paddlepaddle/paddle:1.6.2-gpu-cuda10.0-cudnn7

# please remove --gpus '"device=1"' if you only have one gpu
docker run --name deepspeech2 --rm --gpus '"device=1"' -it -v $(pwd)/models/DeepSpeech:/DeepSpeech -v $(pwd)/audio/:/DeepSpeech/audio/ -v $(pwd)/data/:/DeepSpeech/data/ paddlepaddle/paddle:1.6.2-gpu-cuda10.0-cudnn7 /bin/bash

apt-get update
apt-get install git -y
cd DeepSpeech
sh setup.sh
apt-get install libsndfile1-dev -y
``` 

**in case you found error when running the `setup.sh`**

Error solution for `ImportError: No module named swig_decoders`
```
pip install paddlepaddle-gpu==1.6.2.post107
cd DeepSpeech
pip install soundfile
pip install llvmlite===0.31.0
pip install resampy
pip install python_speech_features

wget http://prdownloads.sourceforge.net/swig/swig-3.0.12.tar.gz
tar xvzf swig-3.0.12.tar.gz
cd swig-3.0.12
apt-get install automake -y 
./autogen.sh
./configure
make
make install

cd ../decoders/swig/
sh setup.sh
cd ../../
```

#### Run Deepspeech2 as an API (inside docker container)
```
pip install flask 

CUDA_VISIBLE_DEVICES=0 python deepspeech2-api.py \
    --mean_std_path='models/librispeech/mean_std.npz' \
    --vocab_path='models/librispeech/vocab.txt' \
    --model_path='models/librispeech' \
    --lang_model_path='models/lm/common_crawl_00.prune01111.trie.klm'
```
Then detach from the docker using ctrl+p & ctrl+q after you see `Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

#### Run Client from the Terminal (outside docker container)

```
docker exec -it deepspeech2 curl http://localhost:5000/transcribe?fpath=audio/google/hello.wav
```

### 3. Wav2letter++

[wav2letter++](https://github.com/facebookresearch/wav2letter) is a highly efficient end-to-end automatic speech recognition (ASR) toolkit written entirely in C++ by Facebook Research, leveraging ArrayFire and flashlight.

Please find the lastest image of [wav2letter's docker](https://hub.docker.com/r/wav2letter/wav2letter/tags).

```
cd models/
mkdir wav2letter
cd wav2letter

for f in acoustic_model.bin tds_streaming.arch decoder_options.json feature_extractor.bin language_model.bin lexicon.txt tokens.txt ; do wget http://dl.fbaipublicfiles.com/wav2letter/inference/examples/model/${f} ; done

ls -sh
cd ../../
```

#### Run docker inference API
```
docker run --name wav2letter -it --rm -v $(pwd)/audio/:/root/host/audio/ -v $(pwd)/models/:/root/host/models/ --ipc=host -a stdin -a stdout -a stderr wav2letter/wav2letter:inference-latest 
```
Then detach from the docker using ctrl+p & ctrl+q 

#### Run Client from the Terminal

```
docker exec -it wav2letter sh -c "cat /root/host/audio/google/hello.wav | /root/wav2letter/build/inference/inference/examples/simple_streaming_asr_example --input_files_base_path /root/host/models/wav2letter/"
```

Detail of [wav2letter++ installation](https://github.com/facebookresearch/wav2letter/wiki#Installation) and [wav2letter++ inference](https://github.com/facebookresearch/wav2letter/wiki/Inference-Run-Examples)


### 4. Wit

[Wit](https://wit.ai/) gives an API interface for ASR. We use [pywit](https://github.com/wit-ai/pywit), the Python SDK for Wit. You need to create an WIT account to get access token.

#### install pywit
```
pip install wit===5.1.0
```

#### Setup Wit access token
```
export WIT_ACCESS_TOKEN=<your Wit access token>
```

#### Check using HTTP API
```
curl -XPOST 'https://api.wit.ai/speech?' \
    -i -L \
    -H "Authorization: Bearer $WIT_ACCESS_TOKEN" \
    -H "Content-Type: audio/wav" \
    --data-binary "@audio/google/hello.wav"
```

**Success Response**
```
HTTP/1.1 100 Continue
Date: Fri, 11 Sep 2020 05:55:51 GMT

HTTP/1.1 200 OK
Content-Type: application/json
Date: Fri, 11 Sep 2020 05:55:52 GMT
Connection: keep-alive
Content-Length: 85

{
  "entities": {},
  "intents": [],
  "text": "hello world google",
  "traits": {}
}
```

#### Trial
```
python models/wit_trial.py
```

## Python Interface for TTSes and ASRs


#### Requirements

```
pip install numpy
pip install pandas
pip install scikit-learn
pip install normalise
```

`normalise` has several nltk data dependencies. Install these by running the following python commands (**inside python**):

```python
import nltk
for dependency in ("brown", "names", "wordnet", "averaged_perceptron_tagger", "universal_tagset"):
    nltk.download(dependency)
```


### TTS

```
python trial.py -t <tts> -o audio/<tts>/icsme.wav
```

**Example on Google**
```
python trial.py -t google -o audio/google/icsme.wav
```


### ASR
```
python trial.py -a <asr> -i audio/<asr>/icsme.wav
```
**Example on Deepspeech2**
```
python trial.py -a paddledeepspeech -i audio/google/icsme.wav
```


## Prepare Europarl Data

We already provided `corpus/europarl-20k.txt` on our Github repository. Thus you can skip this step actually. Please check in the folder `corpus/` to make sure the dataset availability.

If you wanna reproduce how to generate dataset, please follow the next steps

#### 1. Download Raw Data from Kaggle
Download [Eurparl Raw Data](https://www.kaggle.com/djonafegnem/europarl-parallel-corpus-19962011). Then extract it inside the main folder. You will get `europarl-parallel-corpus-19962011/`

#### 2. Generate Corpus
```
python generate_experiment_data.py
```
This code will generate full europarl corpus `corpus/europarl-full.csv` and 20k texts `corpus/europarl-20k.txt` for our experiment.



## Run Without Classifier (RQ1 and RQ2)

```
sh run_without_classifier.sh
```
This script will generate audio files in the form of `audio/without_classifier/<tts>/audio-<id>.wav`. The transcription is saved at `result/without_classifier/<dataset name>/<tts>/<asr>/data.csv`. The statistic (number of failed test case, succuss test case, and indeterminable test case) is saved at `result/without_classifier/<dataset name>/<tts>/<asr>/data.csv`.

## Run With Classifier (RQ2)

#### Setup Classifier

```
pip install torch
pip install simpletransformers
```
#### Trial
```
python try_classifier.py
```
#### Run
```
sh run_with_classifier.sh
```

This script will generate audio files in the form of `audio/with_classifier/<tts>/audio-<id>.wav`. The transcription is saved at `result/with_classifier/<dataset name>/<tts>/<asr>/data.csv`. The statistic (number of failed test case, succuss test case, and indeterminable test case) is saved at `result/with_classifier/<dataset name>/<tts>/<asr>/data.csv`.

## Process 20k Texts (RQ3)

### Generate Audio File

**Template**
```
python generate_audio.py --tts <tts name> --output-dir <output dir location> --lower-bound <lower bound id> --upper-bound <upper bound id>
```

**Example**
```
python generate_audio.py --tts google --output-dir audio/data/ --lower-bound 0 --upper-bound 20000
```

### Recognize Audio File

**Template**
```
python recognize_audio.py --tts <tts name> --asr <asr name> --input-dir <input audio dir location> --output-dir <output transcription dir location> --lower-bound <lower bound id> --upper-bound <upper bound id>
```

**Example**
```
python recognize_audio.py --tts google --asr paddledeepspeech --input-dir audio/data/ --output-dir transcription/ --lower-bound 0 --upper-bound 20000
```

### Please Cite This!
```
@INPROCEEDINGS{Asyrofi2020CrossASR,  
    author={M. H. {Asyrofi} and F. {Thung} and D. {Lo} and L. {Jiang}},  
    booktitle={2020 IEEE International Conference on Software Maintenance and Evolution (ICSME)},
    title={CrossASR: Efficient Differential Testing of Automatic Speech Recognition via Text-To-Speech},   
    year={2020},  volume={},  number={},  
    pages={640-650},  
    doi={10.1109/ICSME46990.2020.00066}}
```



