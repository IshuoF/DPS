# from transformers import  ASTForAudioClassification, ASTConfig,ASTModel
from datasets import load_dataset
import torch
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import LabelEncoder
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
from models import ASTModel


class SpectrogramDataset(Dataset):
    def __init__(self, dataframe):
        self.data = dataframe

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        input_values = torch.tensor(self.data.iloc[idx]['input_values'])
        label = torch.tensor(self.data.iloc[idx]['CDR'])
        return input_values, label


# Load the dataset
with open ("./dataset/spectrograms.json", "r") as file:
    spectrograms = json.load(file)


csv_path = "./dataset/train.csv"
# load the labels from the csv file and extract the CDR column
label_csv = pd.read_csv(csv_path,encoding='latin-1')
label_df = pd.DataFrame(label_csv)
label_df = label_df[["CDR"]]
label_encoder = LabelEncoder()
label_df["CDR"] = label_encoder.fit_transform(label_df["CDR"])


spectrograms_df = pd.DataFrame(spectrograms)
print(spectrograms_df.shape)
spectrograms_df = spectrograms_df.drop(columns=["id"])
spectrograms_df = pd.concat([spectrograms_df , label_df], axis=1)


train_data, test_data = train_test_split(spectrograms_df, test_size=0.2, random_state=42)

train_dataset = SpectrogramDataset(train_data)
test_dataset = SpectrogramDataset(test_data)

batch_size = 4
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

if torch.cuda.is_available():
        device = torch.device("cuda")
        print("Using GPU")
else:
    device = torch.device("cpu")
    print("Using CPU")

model = ASTModel(label_dim=4, fstride=10, tstride=10, input_fdim=128, input_tdim=1024) 
model.to(device)
optimizer = optim.AdamW(model.parameters(), lr=1e-5)
criterion = torch.nn.CrossEntropyLoss()

def train(model, train_loader, optimizer, criterion, epochs=5):
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for batch in tqdm(train_loader, desc=f'Epoch {epoch + 1}/{epochs}', leave=False):
            input_values, labels = batch
            
            input_values, labels = input_values.to(device), labels.to(device)
    
            optimizer.zero_grad()
            logits = model(input_values)
            loss = criterion(logits, labels)  # 注意：在最新版本的transformers中，logits位于logits属性下
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * input_values.size(0)
        epoch_loss = running_loss / len(train_loader.dataset)
        print(f'Train Loss: {epoch_loss:.4f}')

def evaluate(model, test_loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in tqdm(test_loader, desc='Testing', leave=False):
            input_values, labels = batch
            input_values, labels = input_values.to(device), labels.to(device)
            logits = model(input_values)
            _, predicted = torch.max(logits, dim=1)  # 注意：在最新版本的transformers中，logits位于logits属性下
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = correct / total
    print(f'Test Accuracy: {accuracy:.4f}')
    
train(model, train_loader, optimizer, criterion, epochs=50)
torch.save(model.state_dict(), "./saved_models/spec_best_2.pth")
evaluate(model, test_loader)


