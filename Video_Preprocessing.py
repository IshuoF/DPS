import os
import cv2



class Video_Preprocessing():
    def __init__(self, raw_video_path):
        super(Video_Preprocessing, self).__init__()
        self.raw_video_path = raw_video_path
        
    def capture_frames(self):
        cap = cv2.VideoCapture(self.raw_video_path)

        output_folder = os.path.join(os.path.dirname(self.raw_video_path), "frames").replace("\\", "/")
        
        # Check if the video file is opened successfully
        if not cap.isOpened():
            print("Error opening video file")
            return
        
        # Create the output folder if it does not exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        frame_count = 0
    
        print("Frames capture started")
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            frame_count += 1
            frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            
        cap.release()
        print("Frames capture done")
        