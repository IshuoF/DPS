import os
import cv2


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
        
        frame_count = 0
        img_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = total_frames // 100
        print("Frames capture started")
        while True:
            ret, frame = cap.read()

            if not ret:
                break
            if img_count >= 100:
                break
            
            if frame_count % interval == 0:
                frame_path = os.path.join(output_folder, f"frame_{img_count}.jpg")

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
                faces = face_cascade.detectMultiScale(gray, 1.1, 6, 0)

                # Check if faces are detected, if not, continue to the next frame
                if len(faces) == 0:
                    continue

                # Save the first detected face
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
                    face_roi = frame[y:y + h, x:x + w]
                    cv2.imwrite(frame_path, face_roi)
                    img_count += 1
                    break  # Break out of the loop after saving the first detected face

                # Increment frame count only if a face is detected
                frame_count += 1

            else:
                frame_count += 1
            
        cap.release()
        print("Frames capture done")
    
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
    video_preprocessing = Video_Preprocessing("./data/videos/054-GXY/054.MTS")
    video_preprocessing.capture_frames()
    print("Done")