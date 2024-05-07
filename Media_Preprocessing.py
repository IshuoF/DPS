import os
import cv2


import json
import torch,torchaudio
import ffmpeg
import librosa
import numpy as np
import noisereduce as nr
import spafe.features.gfcc as gfcc

from os import environ
from scipy.io import wavfile
from dotenv import load_dotenv
from pydub import AudioSegment
from pyannote.audio import Pipeline
from transformers import AutoFeatureExtractor

class Video_Preprocessing():
    def __init__(self, raw_video_path,output_folder):
        super(Video_Preprocessing, self).__init__()
        self.raw_video_path = raw_video_path
        self.output_folder =  os.path.join(output_folder, "imgs").replace("\\", "/") #/Desktop/Patient/imgs
        
    def capture_frames(self):
        print("Frames capture started")
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        print("Frames capture finished")

class Audio_Preprocessing():
    def __init__(self, raw_video_path,output_folder):
        super(Audio_Preprocessing, self).__init__()
        self.raw_video_path = raw_video_path
        self.output_folder =  os.path.join(output_folder, "audios").replace("\\", "/") #/Desktop/Patient/audios
        self.save_name = 'patient'
    
    def extract_audio(self):
        print("Audio extract started")
        stream = ffmpeg.input(self.raw_video_path)
        audio = stream.audio
        audio_save_name = self.save_name + "_audio.wav"
        audio_output_path = os.path.join(self.output_folder, audio_save_name).replace("\\", "/")
        print(audio_output_path)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        self.audio_ouptut_path = audio_output_path
        audio_output = ffmpeg.output(audio, audio_output_path)
        ffmpeg.run(audio_output)
        print("Audio extract done")
    
       
    def diarization(self):
        print("Diarization started")
        load_dotenv()
        HUGGINGFACE_ACCESS_TOKEN=environ.get("HUGGINGFACE_ACCESS_TOKEN")

        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=HUGGINGFACE_ACCESS_TOKEN)
        
        pipeline.to(torch.device("cuda"))

        # apply pretrained pipeline
        diarization = pipeline(self.audio_ouptut_path,num_speakers=2)

        data = []
        # print the result
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            # print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
            data.append({"start":f"{turn.start:.1f}", "stop":f"{turn.end:.1f}", "speaker":speaker})
        data_output_path = os.path.join(self.output_folder, f"{self.save_name}_diarization_data.json").replace("\\", "/")
        with open(data_output_path, "w") as file:
            file.write(json.dumps(data, indent=3)+"\n")
        print("Diarization done")
        
        self.data = data
        
        return self.data

    def mute_audio_at_time(self):
        print("Mute audio started")
        # with open(os.path.join(self.save_dir, "data.json").replace("\\", "/"), "r") as file:
        #     self.data = json.load(file)
            
        original_audio = AudioSegment.from_file(self.audio_ouptut_path, format="wav")
        speaker = self.data[0]["speaker"]
        
        selected_segments = []
        
        
        for i in range(len(self.data)):
            if self.data[i]["speaker"] == speaker:
                start = float(self.data[i]["stop"]) * 1000
                next_speaker_index = next((j for j in range(i+1, len(self.data)) if self.data[j]["speaker"] == speaker), None)
                if next_speaker_index is not None:
                    end = float(self.data[next_speaker_index]["start"]) * 1000
                else:
                    end = len(original_audio)
                    
                # print(start, end)
                selected_segments.append(original_audio[start:end])
        
        result_audio = sum(selected_segments)
        self.diarization_audio_name = self.save_name + "_diarization_audio.wav"
        sound_output_path = os.path.join(self.output_folder, self.diarization_audio_name).replace("\\", "/")
        result_audio.export(sound_output_path, format="wav")
        print("Mute audio done")

    def noise_reduction(self):
        
        audio_file_path = os.path.join(self.output_folder,self.diarization_audio_name).replace("\\", "/")
        print(audio_file_path)
        print("Noise reduction started")
        
        librosa_audio_data,librosa_sample_rate=librosa.load(audio_file_path)
        
        reduced_noise = nr.reduce_noise(y=librosa_audio_data, sr=librosa_sample_rate,prop_decrease=0.9)
        
        audio_output_path = os.path.join(self.output_folder, f"{self.save_name}_reduced_noise.wav").replace("\\", "/")
        wavfile.write(audio_output_path, librosa_sample_rate, reduced_noise)
        
        sound = AudioSegment.from_file(audio_output_path , format="wav")
        db = sound.dBFS
        def match_target_amplitude(sound, target_dBFS):
            change_in_dBFS = target_dBFS - sound.dBFS
            return sound.apply_gain(change_in_dBFS)
        normalized_sound = match_target_amplitude(sound, db + 5) 
        normalized_sound.export(audio_output_path , format="wav")
    
class Data_Preprocessing():
    def __init__(self, output_folder):
        self.audio_path = os.path.join(output_folder,"audios/patient_reduced_noise.wav").replace("\\", "/")
        self.img_folder = os.path.join(output_folder, "imgs" ).replace("\\", "/")
        
    def get_MGs(self): # MFCCs & GFCCs 
        
        librosa_audio_data,librosa_sample_rate=librosa.load(self.audio_path)
        mfccs_40 = librosa.feature.mfcc(y=librosa_audio_data, sr=librosa_sample_rate, n_mfcc=40)
        mfccs_mean_40= np.mean(mfccs_40.T,axis=0).tolist()
        mfccs_std_40= np.std(mfccs_40.T,axis=0).tolist()
        
        gfccs = gfcc.gfcc(sig=librosa_audio_data,fs=librosa_sample_rate,num_ceps=13)
        gfccs_mean = np.mean(gfccs,axis=0).tolist()
        gfccs_std = np.std(gfccs,axis=0).tolist()
        
        MGs = np.hstack((mfccs_mean_40, mfccs_std_40, gfccs_mean, gfccs_std)).reshape(1,-1)
        print(MGs.shape)
        return MGs
    
    def get_Spectrograms(self):
        feature_extractor = AutoFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
        waveform, sample_rate = torchaudio.load(self.audio_path)
        waveform = waveform.squeeze().numpy()
        inputs = feature_extractor(waveform, sampling_rate=16000, padding="max_length",return_tensors="pt")
        input_values = inputs.input_values
        spectrograms = input_values.view(1024,128)
        
        
        return spectrograms