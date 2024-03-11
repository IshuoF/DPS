from Audio_Preprocessing import Audio_Preprocessing
from Video_Preprocessing import Video_Preprocessing
from datetime import datetime
import os



def main():
    
    # Process all videos in the data folder
    # folder_path = "./data"
    # total_start_time = datetime.now()
    # for root, dirs, files in os.walk(folder_path):
    #     root = root.replace("\\", "/")
    #     for file in files:
    #         if file.endswith(".MTS"):
    #             video_path = os.path.join(root, file)
    #             video_path = video_path.replace("\\", "/")
    #             print(video_path)
                
    #             video_path = os.path.join(root, file)
    #             video_path = video_path.replace("\\", "/")
                
    #             saved_audio_name = file.split(".")[0] + "_audio.wav"
    #             saved_video_name = file.split(".")[0] + "_video.mp4"
    #             saved_audio_path = os.path.join(root, saved_audio_name)
    #             saved_video_path = os.path.join(root, saved_video_name)
                
    #             start_time = datetime.now()
    #             video_preprocessing = Video_Preprocessing(video_path, saved_video_path, saved_audio_path)
    #             video_preprocessing.extract_video_and_audio()
                
    #             audio_preprocessing = Audio_Preprocessing(saved_audio_path, root)
    #             audio_preprocessing.diarization()
    #             audio_preprocessing.mute_audio_at_time()
                
    #             end_time = datetime.now()
    #             execution_time = str(end_time - start_time)
                
    #             print(f"Time taken: {execution_time} s")
                
    # total_end_time = datetime.now()
    # total_execution_time = str(total_end_time - total_start_time)   
    # print(f"Total time taken: {total_execution_time} s")
    
    # Process a single video
    folder_path = "./data/139-YQS"
    
    for file in os.listdir(folder_path):
        
        if file.endswith(".MTS"):
            raw_video_path = os.path.join(folder_path, file).replace("\\", "/")
        
            start_time = datetime.now()
            video_preprocessing = Video_Preprocessing(raw_video_path)
            video_preprocessing.capture_frames()
            
            audio_preprocessing = Audio_Preprocessing(raw_video_path)
            audio_preprocessing.extract_audio()
            audio_preprocessing.diarization()
            audio_preprocessing.mute_audio_at_time()
            end_time = datetime.now()
            
            execution_time = str(end_time - start_time)
                
            print(f"Time taken: {execution_time} s")
         
           
    
    
    
if __name__ == "__main__":
    main()
