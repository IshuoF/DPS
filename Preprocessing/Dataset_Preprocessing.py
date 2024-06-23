import os
import librosa
import json
import numpy as np
import scipy.io.wavfile
import spafe.features.gfcc as gfcc
import parselmouth
import torch, torchaudio
from transformers import ASTFeatureExtractor,AutoFeatureExtractor
from parselmouth.praat import call
import os
import numpy as np
from PIL import Image
from vit_pytorch import ViTs_face
from torchvision import transforms

class Dataset_Preprocessing():
    def __init__(self, audio_folder, img_folder):
        super(Dataset_Preprocessing, self).__init__()
        self.audio_features = []
        self.spectrograms = []
        self.audio_folder = audio_folder
        self.img_folder = img_folder
    
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
        
        
    def get_spectrogram(self):
        print("get_spectrogram")
        
        for root, dirs, files in os.walk(self.audio_folder): 
            for file in files:   
                if file.endswith("reduced_noise.wav"):
                    print(file)
                    feature_extractor = AutoFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
                    
                    audio_file_path = os.path.join(root, file).replace("\\", "/")
                    waveform, sample_rate = torchaudio.load(audio_file_path)
                    waveform = waveform.squeeze().numpy()
                    
                    inputs = feature_extractor(waveform, sampling_rate=16000, padding="max_length",return_tensors="pt")
                    print(inputs)
                    input_values = inputs.input_values
                    input_values = input_values.view(1024,128)
                    print(input_values.shape)
                    data = {
                        "id": audio_file_path.split("/")[-1].split("_")[0],
                        "input_values": input_values.tolist()
                    }
                    
                    self.spectrograms.append(data)
                    
        return self.spectrograms                   
        
    def get_images(self):
        print("get_images")
        face_embedding= []
        images_per_tester = 100
        trans = transforms.Compose([
        transforms.Resize((112, 112)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
        ])
        
        for dirs in os.listdir(self.img_folder):
            print(dirs," start")
            tmp_folder = os.path.join(self.img_folder, dirs)
            
            tester_images = []
            for image_id in range(images_per_tester):
                img_path = os.path.join(tmp_folder,  f"frame_{image_id}.jpg").replace("\\", "/")
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
            model.load_state_dict(torch.load("../pretrained_model/Backbone_VITs_Epoch_2_Batch_12000_Time_2021-03-17-04-05_checkpoint.pth"))
            model.to(device)
            model.eval()
            embeddings = model(tester_images.to(device))
            print("embeddings: ", embeddings.shape)
            embeddings = embeddings.cpu().detach().numpy()
            face_embedding.append(embeddings)    
        
        np.savez(os.path.join("../dataset", "face_dataset.npz"), face_embedding=face_embedding)
        
        
if __name__ == "__main__":
    
    dataset_preprocessing = Dataset_Preprocessing("../data/audios", "../data/imgs")
    dataset_preprocessing.get_images()
   
    
        
  