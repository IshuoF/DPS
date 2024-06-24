# DPS

DPS (Dementia Prediction System) is designed to predict dementia using the Clinical Dementia Rating (CDR) scale, incorporating both visual and verbal features. 
The CDR scale ranges from zero to three: no dementia (CDR = 0), very mild dementia (CDR = 0.5), mild dementia (CDR = 1), 
moderate dementia (CDR = 2), and severe dementia (CDR = 3). For this project, we focus on predictions within the range of zero to two.

## Flow chart
![](https://drive.google.com/u/2/uc?id=1JEmc1UOXNXzs7wF_rctPuTkwxK9ifiJD&export=download)

## Directory Structure

```
.
├── data/
│   ├── audios
│   ├── imgs
│   ├── videos
├── dataset/
├── GUI/
├── models/
├── Preprocessing/
│   ├── Audio_Preprocessing.py
│   ├── Dataset_Preprocessing.py
│   ├── Video_Preprocessing.py
├── pretrained_model/
    ├── Backbone_VITs_Epoch_2_Batch_12000_Time_2021-03-17-04-05_checkpoint.pth
├── saved_models/
│   ├── audio_best.pkl
│   ├── spec_best.pth
│   ├── vit_best.pth
├── main.py
├── Media_Predict_Model.py
├── Media_Preprocessing.py
├── mfccs_train.py
├── face_train.py
├── spe_train.py
├── README.md
├── requirements.txt
├── resources_rc.py
├── ui_function.py
├── ui_main.py

```
### Explanation:
- `data/` - Directory for accessing raw data storage from the lab.
- `dataset/` - Directory for processed data storage.
- `GUI/`  - Directory for GUI icon files and ui design file.
-  `Preprocessing/` - Directory containing preprocessing scripts that handle raw data preparation for training models.

## Usage
### Environment
- Ubuntu 22.04 LTS
- Python 3.11.0


### Setup Instructions
```bash
pip install -r requirments
git clone https://github.com/IshuoF/DPS.git

cd DPS
mkdir saved_models
cd saved_models

# mfccs feature
gdown  'https://drive.google.com/file/d/1Z2R5zs6IISDxGCXzRvf0LaHU9YRU0tfc/view?usp=sharing'

# spectrogram
gdown  'https://drive.google.com/file/d/1JDLuczMVQSleAiHW6d8AdLhach0rp5u_/view?usp=sharing'

# face feature
gdown  'https://drive.google.com/file/d/1fy4Hu7Htk_e4MJIGrFlXIe0APcXQ6_4Z/view?usp=sharing'

cd ..
mkdir pretrained_model
cd pretrained_model

# download pretrained model
gdown 'https://drive.google.com/file/d/1ufPaGt6Zn5j6OlvcRJ3yg6uiaWRLz3K1/view?usp=sharing'
```

## Usage Instructions
```bash
cd DPS
python main.py
```

## Demo 
[![Watch the video](https://img.youtube.com/vi/k4LeckMrtfY/0.jpg)](https://youtu.be/k4LeckMrtfY)

