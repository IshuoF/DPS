import os
import cv2
from deepface import DeepFace

class Video_Preprocessing():
    def __init__(self, raw_video_path,output_folder):
        super(Video_Preprocessing, self).__init__()
        self.raw_video_path = raw_video_path
        self.output_folder =  os.path.join(output_folder, "imgs").replace("\\", "/")
        
    def capture_frames(self):
        cap = cv2.VideoCapture(self.raw_video_path)
        output_folder = self.output_folder
        img_path = self.raw_video_path.split("/")[-1].split(".")[0]
        output_folder = os.path.join(output_folder,img_path).replace("\\", "/")
        print(output_folder)
        # Check if the video file is opened successfully
        if not cap.isOpened():
            print("Error opening video file")
            return
        
        # Create the output folder if it does not exist
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
                
                if count >=76:
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
    
    # def face_detection(self):
    #     # Read the input image 
    #     img = cv2.imread('./data/001-ZZD/frames/frame_1.jpg') 
        
    #     # Convert into grayscale 
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        
    #     # Load the cascade 
    #     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml') 
        
    #     # Detect faces 
    #     faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
    #     # Draw rectangle around the faces and crop the faces 
    #     for (x, y, w, h) in faces: 
    #         cv2.rectangle(img, (x, y-100), (x+w, y+h), (0, 0, 255), 2) 
    #         faces = img[y:y + h, x:x + w] 
    #         cv2.imshow("face",faces) 
    #         cv2.imwrite('face.jpg', faces) 
            
    #     # Display the output 
    #     cv2.imwrite('detcted.jpg', img) 
    #     cv2.imshow('img', img) 
    #     cv2.waitKey()
        
if __name__ == "__main__":
    print("Start")
    # for root, dirs, files in os.walk("../data/videos"): 
    #     for file in files:  
    #         if file.endswith(".MTS"):
    #             if int(file.split(".")[0]) >126:
    #                 video_preprocessing = Video_Preprocessing(os.path.join(root, file).replace("\\", "/"), "../data")
    #                 video_preprocessing.capture_frames()
    video_preprocessing = Video_Preprocessing("../data/videos/006-XSH/006.MTS","../data")
    
    video_preprocessing.capture_frames()
    print("Done")