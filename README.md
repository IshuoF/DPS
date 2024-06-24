# DPS

DPS (Dementia Prediction System) is designed to predict dementia using the Clinical Dementia Rating (CDR) scale, incorporating both visual and verbal features. 
The CDR scale ranges from zero to three: no dementia (CDR = 0), very mild dementia (CDR = 0.5), mild dementia (CDR = 1), 
moderate dementia (CDR = 2), and severe dementia (CDR = 3). For this project, we focus on predictions within the range of zero to two.
# Approach 
(fig)


## Directory Structure
```
.
├── demo.md
├── folder
│   ├── file1.html
│   └── file2.html
├── img
│   ├── img1.png
│   └── img2.png
└── index.html
```

# Usage
## Environment
Ubuntu 22.04 LTS

Pyhton 3.11.9


## Setup Instructions
```python
pip install -r requirments
git clone https://github.com/IshuoF/DPS.git

cd DPS
mkdir saved_models
cd saved_models

## mfccs feature
gdown  'https://drive.google.com/file/d/1Z2R5zs6IISDxGCXzRvf0LaHU9YRU0tfc/view?usp=sharing'

## spectrogram
gdown  'https://drive.google.com/file/d/1JDLuczMVQSleAiHW6d8AdLhach0rp5u_/view?usp=sharing'

## face feature
gdown  'https://drive.google.com/file/d/1fy4Hu7Htk_e4MJIGrFlXIe0APcXQ6_4Z/view?usp=sharing'

cd ..
mkdir pretrained_model
cd pretrained_model

## download pretrained model
gdown 'https://drive.google.com/file/d/1ufPaGt6Zn5j6OlvcRJ3yg6uiaWRLz3K1/view?usp=sharing'
```

## Usage Instructions
```python
cd DPS
python main.py
```
# Demo 
[![Watch the video](https://img.youtube.com/vi/k4LeckMrtfY/0.jpg)](https://youtu.be/k4LeckMrtfY)

