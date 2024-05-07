

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog
import os
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
# from Preprocessing.Video_Preprocessing import Video_Preprocessing
# from Preprocessing.Audio_Preprocessing import Audio_Preprocessing
# from Preprocessing.Dataset_Preprocessing import Dataset_Preprocessing

from Media_Preprocessing import * 
from Media_Predict_Model import * 

class AnalysisThread(QThread):
    progress_updated = pyqtSignal(int)

    def __init__(self, backend):
        super().__init__()
        self.backend = backend

    def run(self):
        self.backend.analyze()

    def update_progress(self, progress):
        self.progress_updated.emit(progress)


class Backend:
    def __init__(self, main_window):
        self.output_folder = None
        self.main_window = main_window.ui if hasattr(main_window, 'ui') else main_window
        self.analysis_thread = AnalysisThread(self)
        self.analysis_thread.finished.connect(self.analysis_finished)
        self.analysis_thread.progress_updated.connect(self.update_progress)
        
        
    def load_video(self):
        self.raw_video_path, _ = QFileDialog.getOpenFileName(None, 'Select Video')
        
        if self.raw_video_path == "":
            print("No video selected")
        else:
            print("Video loaded")
            self.main_window.label_select_video.setText("影片已選擇")
            self.main_window.Button_start_analyze.setEnabled(True)
            self.main_window.Button_start_analyze.setStyleSheet("QPushButton{"
                                                    "border-radius: 30px;"
                                                    "background-color: rgb(253, 237, 93);"
                                                    "font:  20pt \"微軟正黑體\"; "
                                                    "}"
                                                    
                                                    "QPushButton:hover{"
                                                    "border:1px solid;"
                                                    "border-color:  rgb(255, 239, 116);"
                                                    "background-color:  rgb(255, 249, 56);"
                                                    "}"
                                                    )

    def start_analysis(self):
        print("Analysis started!")
        self.main_window.Button_select_video.hide()
        self.main_window.Button_start_analyze.hide()
        self.main_window.label_select_video.hide()
        
        self.main_window.label_status.show()
        self.main_window.label_loading.show()
        self.main_window.progress_bar.show()
        self.main_window.progress_bar.setValue(0)
        
        self.main_window.label_loading.setText("LOADING...")
        
        self.output_folder = "C:/Users/USER/Desktop/Patient"
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(900) #Add a timer to update the progress bar
        self.analysis_thread.start()
        
       
        
    def analyze(self):
        

        
        start_time = datetime.now()  
        video_preprocessing = Video_Preprocessing(self.raw_video_path,output_folder=self.output_folder)
        self.main_window.label_status.setText("影像處理中...")
        video_preprocessing.capture_frames()
        
        audio_preprocessing = Audio_Preprocessing(self.raw_video_path,output_folder=self.output_folder)
        self.main_window.label_status.setText("音訊處理中...")
        audio_preprocessing.extract_audio()
        audio_preprocessing.diarization()
        audio_preprocessing.mute_audio_at_time()
        audio_preprocessing.noise_reduction()
        
        self.main_window.label_status.setText("程式分析中...")
        
        # audio_path = os.path.join(self.output_folder,"audios").replace("\\", "/")
        # img_path = os.path.join(self.output_folder,"imgs").replace("\\", "/")

        # data_preprocessing = Dataset_Preprocessing(audio_path, img_path)
        # features = data_preprocessing.get_audio_features()
        # extracted_features_df=pd.DataFrame(features)
        # mfccs_mean_40 = np.array(extracted_features_df["mfccs_mean_40"].to_list())
        # mfccs_std_40 = np.array(extracted_features_df["mfccs_std_40"].tolist())
        # gfccs_mean = np.array(extracted_features_df["gfccs_mean"].tolist())
        # gfccs_std = np.array(extracted_features_df["gfccs_std"].tolist())
        # patient_data = np.hstack((mfccs_mean_40, mfccs_std_40, gfccs_mean, gfccs_std))
        
        # print(patient_data.shape)
        # with open('./saved_models/audio_rf_model.pkl', 'rb') as f:
        #     loaded_model = pickle.load(f)
            
        # predicted_class = loaded_model.predict(patient_data)  
        # print(predicted_class)
        
        data_preprocessing = Data_Preprocessing (self.output_folder)
        print("MGS")
        MGs_data = data_preprocessing.get_MGs()
        print("Spectrogram")
        Spectrogram_data = data_preprocessing.get_Spectrograms()
        MGs_predict = Media_Predict_Model().MGs_predict_model(MGs_data)
        Spectrogram_predict = Media_Predict_Model().Spectrogram_predict_model(Spectrogram_data)
        
        print("MGs_predict" , MGs_predict)
        print("Spectrogram_predict" ,Spectrogram_predict)
        
        end_time = datetime.now()
        
        execution_time = str(end_time - start_time)
            
        print(f"Time taken: {execution_time} s")
        self.main_window.progress_bar.setValue(100)
        
        
        # if predicted_class == 0:
        #     result =  "沒有失智" 
        # elif predicted_class == 1:
        #     result = "未確定"
        # elif predicted_class == 2:
        #     result =  "輕度失智"
        # else:
        #     result = "中度失智"
        
        
        self.main_window.label_status.hide()
        self.main_window.progress_bar.hide()
        self.main_window.label_loading.hide()
        self.main_window.label_origin_CDR.show()
        self.main_window.label_predict_CDR.show()
        self.main_window.label_show_save.show()
        
        
        # self.main_window.label_predict_CDR.setText(f"程式分析預測結果 : {result}")
        # self.main_window.label_origin_CDR.setText(f"醫院診斷結果 : {result}")
        self.main_window.label_show_save.setText("分析完成，結果儲存至桌面資料夾")
        
 
        
    def update_progress(self):
        if int(self.main_window.progress_bar.value()) >= 80:
            self.progress_timer.stop()
        else:
            self.main_window.progress_bar.setValue(self.main_window.progress_bar.value() + 1)
                  
    def analysis_finished(self):
        # 在這裡更新 GUI，例如更新進度條狀態、顯示分析結果等
        self.main_window.progress_bar.setValue(100)
        print("Analysis End!")
   