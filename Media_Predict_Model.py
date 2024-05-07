import torch
import pickle
from models import ASTModel

class Media_Predict_Model:
    def __init__(self):
        pass
        
    def MGs_predict_model(self,patient_data):
        print("MGs_predict_model started")
        with open('./saved_models/audio_rf_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        predicted_class = model.predict(patient_data)
        print("MGs_predict_model finished")
        return predicted_class
        
    
    def Spectrogram_predict_model(self,spectrograms):
        print("Spectrogram_predict_model started")
        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("Using GPU")
        else:
            device = torch.device("cpu")
            print("Using CPU")
            
        model = ASTModel(label_dim=4, fstride=10, tstride=10, input_fdim=128, input_tdim=1024)
        model.load_state_dict(torch.load("./saved_models/spec_best.pth"))
        model.to(device)
        
        with torch.no_grad():
            model.eval()
            input_values = torch.tensor(spectrograms).unsqueeze(0).to(device)
            output = model(input_values)
            _, predicted = torch.max(output, dim=1)
            predicted_class = predicted
            
        print("Spectrogram_predict_model finished")
        return predicted_class
        