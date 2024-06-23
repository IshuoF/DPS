import os
import cv2
from deepface import DeepFace
import matplotlib.pyplot as plt
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

from PIL import Image
from vit_pytorch import ViTs_face
from torchvision import transforms

class Video_Preprocessing():
    def __init__(self, raw_video_path,output_folder):
        super(Video_Preprocessing, self).__init__()
        self.raw_video_path = raw_video_path
        self.output_folder =  os.path.join(output_folder, "imgs").replace("\\", "/") #/Desktop/Patient/imgs
        
    def capture_frames(self):
        print("Frames capture started")
        os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
        output_folder = self.output_folder + '/frames'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        count = 0
        frame_number = 0
        
        cap = cv2.VideoCapture(self.raw_video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = total_frames // 100

        while True:
            ret, frame = cap.read()
            
            if frame_number % interval == 0:
                frame_path = os.path.join(output_folder, f"frame_{count}.jpg").replace("\\", "/")
                
                result= DeepFace.extract_faces(frame, detector_backend = 'mtcnn',align=True)
                
                face_info = result[0]['facial_area']
                x, y, w, h = face_info['x'],face_info['y'],face_info['w'],face_info['h']
                face = frame[y:y+h, x:x+w]
                face = cv2.resize(face, (224, 224))
                cv2.imwrite(frame_path, face)
                count += 1
            
            frame_number += 1

            if count == 100:
                break
        cap.release()
        print("Frames capture finished")

    def face_recongnition(self):
        print("Face recognition started")
        os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
        input_folder = self.output_folder + '/frames'
        imgs = []
        for i in range(100):
            img_path = os.path.join(input_folder, f"frame_{i}.jpg").replace("\\", "/")
            imgs.append(img_path)
        
        output_folder = self.output_folder + '/extract_faces' 
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        count = 0
        for img in imgs:
       
            result= DeepFace.extract_faces(img, detector_backend = 'mtcnn',align=True)
            
            face_info = result[0]['facial_area']
            x = face_info['x']
            y = face_info['y']
            w = face_info['w']
            h = face_info['h']
            # print(x, y, w, h)
            image = cv2.imread(img)
            face = image[y:y+h, x:x+w]
            face = cv2.resize(face, (224, 224))
            cv2.imwrite(os.path.join(output_folder, f"face_{count}.jpg").replace("\\", "/"), face)
               
            count += 1
        
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
            
            data.append({"start":f"{turn.start:.1f}", "stop":f"{turn.end:.1f}", "speaker":speaker})
        data_output_path = os.path.join(self.output_folder, f"{self.save_name}_diarization_data.json").replace("\\", "/")
        
        with open(data_output_path, "w") as file:
            file.write(json.dumps(data, indent=3)+"\n")
        print("Diarization done")
        
        self.data = data
        
        return self.data

    def mute_audio_at_time(self):
        print("Mute audio started")
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
        print("Noise reduction started")
        
        librosa_audio_data,librosa_sample_rate=librosa.load(audio_file_path)
        
        reduced_noise = nr.reduce_noise(y=librosa_audio_data, sr=librosa_sample_rate,prop_decrease=0.9)
        
        audio_output_path = os.path.join(self.output_folder, f"{self.save_name}_reduced_noise.wav").replace("\\", "/")
        wavfile.write(audio_output_path, librosa_sample_rate, reduced_noise)
        
        sound = AudioSegment.from_file(audio_output_path , format="wav")
        db = sound.dBFS
        
        ## Normalize the audio
        def match_target_amplitude(sound, target_dBFS):
            change_in_dBFS = target_dBFS - sound.dBFS
            return sound.apply_gain(change_in_dBFS)
        
        normalized_sound = match_target_amplitude(sound, db + 5) 
        normalized_sound.export(audio_output_path , format="wav")
    
class Data_Preprocessing():
    def __init__(self, output_folder):
        self.audio_path = os.path.join(output_folder,"audios/patient_reduced_noise.wav").replace("\\", "/")
        self.img_folder = os.path.join(output_folder, "imgs/frames" ).replace("\\", "/")
        
    def get_MGs(self): # MFCCs & GFCCs 
        
        librosa_audio_data,librosa_sample_rate=librosa.load(self.audio_path)
        mfccs_40 = librosa.feature.mfcc(y=librosa_audio_data, sr=librosa_sample_rate, n_mfcc=40)
        mfccs_mean_40= np.mean(mfccs_40.T,axis=0).tolist()
        mfccs_std_40= np.std(mfccs_40.T,axis=0).tolist()
        
        gfccs = gfcc.gfcc(sig=librosa_audio_data,fs=librosa_sample_rate,num_ceps=13)
        gfccs_mean = np.mean(gfccs,axis=0).tolist()
        gfccs_std = np.std(gfccs,axis=0).tolist()
        
        MGs = np.hstack((mfccs_mean_40, mfccs_std_40, gfccs_mean, gfccs_std)).reshape(1,-1)
        return MGs
    
    def get_Spectrograms(self):
        feature_extractor = AutoFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
        waveform, sample_rate = torchaudio.load(self.audio_path)
        waveform = waveform.squeeze().numpy()
        inputs = feature_extractor(waveform, sampling_rate=16000, padding="max_length",return_tensors="pt")
        input_values = inputs.input_values
        spectrograms = input_values.view(1024,128)

        return spectrograms
    
    def get_Faces(self):
        face_embedding= []
        trans = transforms.Compose([
        transforms.Resize((112, 112)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
        ])
        tester_images = []
        images_per_tester = 100
        for image_id in range(images_per_tester):
            img_path = os.path.join(self.img_folder,  f"frame_{image_id}.jpg").replace("\\", "/")
            img = Image.open(img_path)
            img = trans(img)
            tester_images.append(img)

        tester_images = torch.stack(tester_images)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = ViTs_face(
                loss_type='CosFace',
                GPU_ID=device,
                num_class=93431,
                image_size=112,
                patch_size=8,
                ac_patch_size=12,
                pad=4,
                dim=512,
                depth=20,
                heads=8,
                mlp_dim=2048,
                dropout=0.1,
                emb_dropout=0.1
            )
        model.load_state_dict(torch.load("./pretrained_model/Backbone_VITs_Epoch_2_Batch_12000_Time_2021-03-17-04-05_checkpoint.pth"))
        model.to(device)
        model.eval()
        embeddings = model(tester_images.to(device))
        print("embeddings: ", embeddings.shape)
        embeddings = embeddings.cpu().detach().numpy()
        face_embedding = embeddings
        
        return face_embedding