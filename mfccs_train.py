import os
import json
import pandas as pd
import numpy as np
import pickle
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score



json_path = "./dataset/audio_features.json"
csv_path = "./dataset/train.csv"


with open(json_path, "r") as file:
    features = json.load(file)

# load the labels from the csv file and extract the CDR column
label_csv = pd.read_csv(csv_path,encoding='latin-1')
label_df = pd.DataFrame(label_csv)
label_df = label_df[["CDR"]]


# concatenate the extracted features and the labels
extracted_features_df=pd.DataFrame(features)
extracted_features_df = pd.concat([extracted_features_df, label_df], axis=1)

# compare the CDR column with the extracted features
# extracted_features_df = pd.concat([extracted_features_df.loc[extracted_features_df["CDR"]==0,:], extracted_features_df.loc[extracted_features_df["CDR"]==0.5,:]] ,axis=0)

# extract the features and the labels
id = extracted_features_df["id"].to_numpy()
cdr = extracted_features_df["CDR"].to_numpy()
mfccs_mean_40 = np.array(extracted_features_df["mfccs_mean_40"].to_list())
mfccs_std_40 = np.array(extracted_features_df["mfccs_std_40"].tolist())
gfccs_mean = np.array(extracted_features_df["gfccs_mean"].tolist())
gfccs_std = np.array(extracted_features_df["gfccs_std"].tolist())
mfccs_mean_20 = np.array(extracted_features_df["mfccs_mean_20"].tolist())
mfccs_std_20 = np.array(extracted_features_df["mfccs_std_20"].tolist())
mfccs_mean_13 = np.array(extracted_features_df["mfccs_mean_13"].tolist())
mfccs_std_13 = np.array(extracted_features_df["mfccs_std_13"].tolist())
f0_mean = extracted_features_df["f0_mean"].to_numpy()
f0_stdev = extracted_features_df["f0_stdev"].to_numpy()
hnr = extracted_features_df["hnr"].to_numpy()
jitter = extracted_features_df["jitter"].to_numpy()
shimmer = extracted_features_df["shimmer"].to_numpy()   


extracted_features_df = np.hstack((mfccs_mean_40, mfccs_std_40, gfccs_mean, gfccs_std))
print(extracted_features_df.shape)

label_encoder = LabelEncoder()
X = extracted_features_df
y = label_encoder.fit_transform(cdr)



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

y_pred = rf_classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy}")


with open('audio_rf_model.pkl', 'wb') as f:
    pickle.dump(rf_classifier, f)