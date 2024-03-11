import os
import json
import torch
import ffmpeg
from os import environ
from dotenv import load_dotenv
from pydub import AudioSegment
from pyannote.audio import Pipeline


class Audio_Preprocessing():
    def __init__(self, raw_video_path):
        super(Audio_Preprocessing, self).__init__()
        self.raw_video_path = raw_video_path
        self.output_folder = os.path.dirname(self.raw_video_path)
        self.save_name = self.raw_video_path.split("/")[-1].split(".")[0]
    
    def extract_audio(self,):
        print("Audio extract started")
        stream = ffmpeg.input(self.raw_video_path)
        audio = stream.audio
        audio_save_name = self.save_name + "_audio.wav"
        audio_output_path = os.path.join(self.output_folder, audio_save_name).replace("\\", "/")
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
            # print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
            
            data.append({"start":f"{turn.start:.1f}", "stop":f"{turn.end:.1f}", "speaker":speaker})
        
        
        # new_data = []
        # new_data.append(data[0])
        # for i in range(1,len(data)):
        #     if data[i]["speaker"] == data[i-1]["speaker"]:
        #         new_data[-1]["stop"] = data[i]["stop"]
        #     else:
        #         new_data.append(data[i]) 
        
        data_output_path = os.path.join(self.output_folder, "data.json").replace("\\", "/")
        with open(data_output_path, "w") as file:
            file.write(json.dumps(data, indent=3)+"\n")
        print("Diarization done")
        
        self.data = data
        
        return self.data

    def mute_audio_at_time(self):
        print("Mute audio started")
        # with open(os.path.join(self.save_dir, "data.json").replace("\\", "/"), "r") as file:
        #     self.data = json.load(file)
            
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
                    
                print(start, end)
                selected_segments.append(original_audio[start:end])
        
        result_audio = sum(selected_segments)  
        processed_audio_name = self.save_name + "_processed_audio.wav"
        sound_output_path = os.path.join(self.output_folder, processed_audio_name).replace("\\", "/")
        result_audio.export(sound_output_path, format="wav")
        print("Mute audio done")

        