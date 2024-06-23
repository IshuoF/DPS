import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from tqdm import tqdm
from models import fusion_face_ast
from transformers import ViTFeatureExtractor, ViTForImageClassification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

class FaceDataset(Dataset):
    def __init__(self, images ,labels,transform=None):
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]
        
        if self.transform:
            
            # 应用变换
            image = self.transform(image)
        
        return image, label


    
csv_path = "./dataset/train.csv"
# load the labels from the csv file and extract the CDR column
label_csv = pd.read_csv(csv_path,encoding='latin-1')
label_df = pd.DataFrame(label_csv)
label_df = label_df[["CDR"]]
label_encoder = LabelEncoder()
label_df["CDR"] = label_encoder.fit_transform(label_df["CDR"])

print(label_df.shape)

faces_data = np.load("./dataset/face_dataset.npz", allow_pickle=True)
faces = faces_data['face_embedding']
print(faces.shape)

X_train, X_test, y_train, y_test = train_test_split(faces, label_df.values, test_size=0.2, stratify=label_df.values, random_state=42)
train_dataset = FaceDataset(X_train, y_train, transform=transforms.ToTensor())
test_dataset = FaceDataset(X_test, y_test, transform=transforms.ToTensor())

print(len(train_dataset), len(test_dataset))
print(train_dataset.images.shape)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = fusion_face_ast.FusionModel(v_input_size = 512, hidden_size=512, num_layers=2, num_classes=4)
model.to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-4)
criterion = nn.CrossEntropyLoss()
num_epochs = 400

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)


model.train()
for epoch in range(num_epochs):
    running_loss = 0.0
    for i, (images, labels) in tqdm(enumerate(train_loader, 0)):
        
        images = images.squeeze(axis=1)
        images_torch, labels_torch = images.clone().detach(), labels.clone().detach()
        images_torch, labels_torch = images_torch.to(device), labels_torch.to(device).view(-1)
        optimizer.zero_grad()
        outputs,_ = model(images_torch)
        loss = criterion(outputs, labels_torch)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {running_loss / len(train_loader)}")

# 保存微调后的模型
torch.save(model.state_dict(), './saved_models/vit_model.pth')

# 评估模型
model.eval()
correct = 0
total = 0
with torch.no_grad():
     for i, (images, labels) in tqdm(enumerate(test_loader, 0)):
        images = images.squeeze(axis=1) 
        images_torch, labels_torch = images.clone().detach(), labels.clone().detach()
        images_torch, labels_torch = images_torch.to(device), labels_torch.to(device).view(-1)
        outputs,_ = model(images_torch)
        _, predicted = torch.max(outputs, 1)
        total += labels_torch.size(0)
        correct += (predicted == labels_torch).sum().item()

print(f"Accuracy on test set: {100 * correct / total}%")