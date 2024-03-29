import os
import json
import librosa
import numpy as np
import pandas as pd
import scipy.io.wavfile
import spafe.features.gfcc as gfcc
import parselmouth
from parselmouth.praat import call


class dataset_Preprocessing():
    def __init__(self):
        super(dataset_Preprocessing, self).__init__()
        self.audio_features = []
        self.audio_folder = "./data/audios"
        self.img_folder = "./data/imgs"
    
    def get_audio_features(self):
        for root, dirs, files in os.walk(self.audio_folder): 
            for file in files:   
                if file.endswith("reduced_noise.wav"):
                    audio_file_path = os.path.join(root, file).replace("\\", "/")
                    print(audio_file_path)
                    librosa_audio_data,librosa_sample_rate=librosa.load(audio_file_path)
                    
                    mfccs_40 = librosa.feature.mfcc(y=librosa_audio_data, sr=librosa_sample_rate, n_mfcc=40)
                    mfccs_mean_40= np.mean(mfccs_40.T,axis=0) #40
                    mfccs_std_40= np.std(mfccs_40.T,axis=0)
                    
                    mfccs_20 = librosa.feature.mfcc(y=librosa_audio_data, sr=librosa_sample_rate, n_mfcc=20)
                    mfccs_mean_20= np.mean(mfccs_20.T,axis=0) #20
                    mfccs_std_20= np.std(mfccs_20.T,axis=0)
                    
                    mfccs_13 = librosa.feature.mfcc(y=librosa_audio_data, sr=librosa_sample_rate, n_mfcc=13)
                    
                    mfccs_mean_13= np.mean(mfccs_13.T,axis=0) #40
                    mfccs_std_13= np.std(mfccs_13.T,axis=0)
                    
                    
                    f0, voiced_flag, voiced_probs = librosa.pyin(librosa_audio_data,
                                                                fmin=librosa.note_to_hz('C2'),
                                                                fmax=librosa.note_to_hz('C7'))
                    
                    sound = parselmouth.Sound(audio_file_path)
                    pitch = call(sound, "To Pitch", 0.0, 75, 600)
                    f0_mean = call(pitch, "Get mean", 0, 0, "Hertz")
                    f0_stdev = call(pitch, "Get standard deviation", 0, 0, "Hertz")
                    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0_mean, 0.1, 1.0)
                    hnr = call(harmonicity, "Get mean", 0, 0)
                    pointProcess = call(sound, "To PointProcess (periodic, cc)", 75, 600)
                    jitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
                    shimmer = call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
                    
                    fs, sig = scipy.io.wavfile.read(audio_file_path)
                    gfccs = gfcc.gfcc(sig=sig,fs=fs,num_ceps=13)
                    gfccs_mean = np.mean(gfccs,axis=0) #13
                    gfccs_std = np.std(gfccs,axis=0)
                    # data = np.concatenate((mfccs_mean, mfccs_std, gfccs_mean, gfccs_std,[jitter], [shimmer], [f0_mean], [f0_stdev], [hnr]),axis=0)
                    print(audio_file_path.split("/")[-1].split("_")[0])
                    data = {
                        "id": audio_file_path.split("/")[-1].split("_")[0],
                        "mfccs_mean_40": mfccs_mean_40.tolist(),
                        "mfccs_std_40": mfccs_std_40.tolist(),
                        "mfccs_mean_20": mfccs_mean_20.tolist(),
                        "mfccs_std_20": mfccs_std_20.tolist(),
                        "mfccs_mean_13": mfccs_mean_13.tolist(),
                        "mfccs_std_13": mfccs_std_13.tolist(),
                        "gfccs_mean": gfccs_mean.tolist(),
                        "gfccs_std": gfccs_std.tolist(),
                        "f0": f0.tolist(),
                        "jitter": jitter,
                        "shimmer": shimmer,
                        "f0_mean": f0_mean,
                        "f0_stdev": f0_stdev,
                        "hnr": hnr
                    }
                    # print(mfccs_mean, mfccs_std, gfccs_mean, gfccs_std,f0, jitter, shimmer, f0_mean, f0_stdev, hnr)
                    self.audio_features.append(data)  
                    
        return self.audio_features             
        
       
if __name__ == "__main__":
    features = []
    dataset_preprocessing = dataset_Preprocessing()
    features = dataset_preprocessing.get_audio_features()
    with open("./dataset/audio_features.json", "w") as file:
        json.dump(features, file, indent=4)
        
    extracted_features_df = pd.DataFrame(features)
    print(extracted_features_df.head())
  