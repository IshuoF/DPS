from ui_main import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow,QPushButton,QApplication,QFileDialog
from PySide6.QtCore import Qt,QThread,Signal,QTimer
from datetime import datetime
from Media_Preprocessing import * 
from Media_Predict_Model import * 
import os
import shutil
import sqlite3
from PySide6.QtWidgets import QTableWidgetItem

def delete_folder_in_directory(directory, subdirectories):
        try:
            
            for subdirectory in subdirectories:
                
                subdirectory_path = os.path.join(directory, subdirectory)
                
                # 检查子目录是否存在
                if os.path.exists(subdirectory_path):
                   
                    shutil.rmtree(subdirectory_path)
                    print(f"Deleted subdirectory and all its contents: {subdirectory_path}")
                else:
                    print(f"Subdirectory does not exist: {subdirectory_path}")
                    
        except Exception as e:
            print(f"An error occurred: {e}")



class AnalysisThread(QThread):
    progress_updated = Signal(int)

    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow

    def run(self):
        self.MainWindow.analyze()

    def update_progress(self, progress):
        self.progress_updated.emit(progress)



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # switch to different pages
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.sidemenu_visible.setHidden(True)
        self.home_hide.clicked.connect(self.switch_to_home)
        self.home_vis.clicked.connect(self.switch_to_home)
        self.platform_hide.clicked.connect(self.switch_to_platform)
        self.platform_vis.clicked.connect(self.switch_to_platform)
        self.history_hide.clicked.connect(self.switch_to_history)
        self.history_vis.clicked.connect(self.switch_to_history)
        self.info_hide.clicked.connect(self.switch_to_info)
        self.info_vis.clicked.connect(self.switch_to_info)
        
        self.output_folder = "C:/Users/USER/Desktop/Patient"
        self.database = "C:/Users/USER/Desktop/Patient/predictions.sqlite"
        # thread
        self.analysis_thread = AnalysisThread(self)
        self.analysis_thread.finished.connect(self.analysis_finished)
        self.analysis_thread.progress_updated.connect(self.update_progress)
        
        # button
        self.Button_select_video.clicked.connect(self.load_video)
        self.Button_start_analyze.clicked.connect(self.start_analysis)
        self.Button_restart.clicked.connect(self.restart)
        self.button_search_history.clicked.connect(self.query_predictions)
        # database
        self.init_database()
        
        ## timer
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.execution_timer = QTimer()
        self.execution_timer.timeout.connect(self.update_execution_time) 
        
    # Switch to different pages
        
    def switch_to_home(self):
        self.stackedWidget.setCurrentIndex(0)
    
    def switch_to_platform(self):
        self.stackedWidget.setCurrentIndex(1)
    
    def switch_to_history(self):
        self.stackedWidget.setCurrentIndex(2)
    
    def switch_to_info(self):
        self.stackedWidget.setCurrentIndex(3)
    
    # Database
    def init_database(self):
        if not os.path.exists(self.database):
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    patient_name TEXT,
                    CDR TEXT,
                    face_predict TEXT,
                    mgs_predict TEXT,
                    timestamp TEXT
                )
            ''')
            self.conn.commit()
            self.conn.close()
            print("Database predictions.sqlite created successfully.")
        else:
            print("Database predictions.sqlite already exists.")
        
    def query_predictions(self):
        try:
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM predictions")
            rows = self.cursor.fetchall()
            self.history_table.setRowCount(len(rows))
            tablerow = 0
            for row in rows:
                self.history_table.setItem(tablerow, 0, QTableWidgetItem(row[0]))
                self.history_table.setItem(tablerow, 1, QTableWidgetItem(row[1]))
                self.history_table.setItem(tablerow, 2, QTableWidgetItem(row[2]))
                self.history_table.setItem(tablerow, 3, QTableWidgetItem(row[3]))
                self.history_table.setItem(tablerow, 4, QTableWidgetItem(row[4]))
                
                tablerow += 1
                print(row)
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")
            
    # BackEnd
    def load_video(self):
        self.raw_video_path, _ = QFileDialog.getOpenFileName(None, 'Select Video')
        
        if self.raw_video_path == "":
            print("No video selected")
        else:
            print("Video loaded")
            self.label_select_video.setText("影片已選擇")
            self.Button_start_analyze.setEnabled(True)
            self.Button_start_analyze.setStyleSheet("QPushButton{"
                                                    "border-radius: 40px;"
                                                    "background-color: rgb(255, 209, 41);"
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
        self.Button_select_video.hide()
        self.Button_start_analyze.hide()
        self.label_select_video.hide()
        
        self.label_status.show()
        self.progressBar.show()
        self.progressBar.setValue(0)
        self.label_show_execution_time.show()

        self.progress_timer.start(2300) #Add a timer to update the progress bar
        self.execution_timer.start(1000)  # Update every second
        self.analysis_thread.start()

        
    
    def analyze(self):

        self.start_time = datetime.now()  
        
        ## Media Preprocessing 
        video_preprocessing = Video_Preprocessing(self.raw_video_path,output_folder=self.output_folder)
        self.label_status.setText("影像處理中...")
        video_preprocessing.capture_frames()
        # video_preprocessing.face_recongnition()
        
        audio_preprocessing = Audio_Preprocessing(self.raw_video_path,output_folder=self.output_folder)
        self.label_status.setText("音訊處理中...")
        audio_preprocessing.extract_audio()
        audio_preprocessing.diarization()
        audio_preprocessing.mute_audio_at_time()
        audio_preprocessing.noise_reduction()
        
        self.label_status.setText("程式分析中...")
        
        ## Data Preprocessing
        data_preprocessing = Data_Preprocessing (self.output_folder)
        MGs_data = data_preprocessing.get_MGs()
        self.progressBar.setValue(85)
        Spectrogram_data = data_preprocessing.get_Spectrograms()
        self.progressBar.setValue(90)
        face_data = data_preprocessing.get_Faces()
        self.progressBar.setValue(95)
        
        ## Predict Result
        MGs_predict = Media_Predict_Model().MGs_predict_model(MGs_data)
        Spectrogram_predict = Media_Predict_Model().Spectrogram_predict_model(Spectrogram_data)
        Face_predict = Media_Predict_Model().Face_predict_model(face_data)
        
        print("MGs_predict" , MGs_predict)
        print("Spectrogram_predict" ,Spectrogram_predict)
        print("Face_predict" ,Face_predict)
        
        end_time = datetime.now()
        execution_time = str(end_time - self.start_time).split(".")[0]
        print(f"Time taken: {execution_time} s")
        self.progressBar.setValue(100)
        
        final_CDR = int((int(MGs_predict) + int(Spectrogram_predict) + int(Face_predict)) / 3)
        
        if final_CDR == 0:
            final_CDR = 0
        elif final_CDR == 1:
            final_CDR = 0.5
        elif final_CDR == 2:
            final_CDR = 1
        else:
            final_CDR = 2
        
        def covert_to_class(predicted_class):
            if predicted_class == 0:
                return "沒有失智"
            elif predicted_class == 1:
                return "未確定"
            elif predicted_class == 2:
                return "輕度失智"
            else:
                return "中度失智"
        
        MGs_predict = covert_to_class(MGs_predict)
        Spectrogram_predict = covert_to_class(Spectrogram_predict)
        Face_predict = covert_to_class(Face_predict)
        
        
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        patient_name = "Patient Name"  # You can replace this with an actual patient name if available
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO predictions (patient_name, CDR, face_predict, mgs_predict, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (patient_name, final_CDR,Face_predict,MGs_predict,timestamp))
        conn.commit()
        conn.close()
        
        self.label_status.hide()
        self.progressBar.hide()
        self.execution_timer.stop()
        self.label_show_execution_time.hide()
        self.label_origin_CDR.show()
        self.label_visual_predict.show()                                        
        self.label_mfcc_predict.show()
        self.label_show_save.show()
        self.Button_restart.show()
        self.label_show_final_execution_time.show()
        self.label_show_final_execution_time.setText(f"執行時間 : {execution_time}")
        
        self.label_visual_predict.setText(f"視訊分析預測結果 : {Face_predict}")
        self.label_mfcc_predict.setText(f"音訊分析預測結果 : {MGs_predict }")
        self.label_origin_CDR.setText(f"醫院診斷結果 : {MGs_predict }")
        self.label_show_save.setText("分析完成，結果儲存至桌面資料夾")
        
        delete_folder_in_directory(self.output_folder,['audios','imgs'])
        
 
    def restart(self):  
        self.label_visual_predict.hide()
        self.label_mfcc_predict.hide()
        self.label_origin_CDR.hide()
        self.label_show_save.hide()
        self.Button_restart.hide()
        self.label_show_final_execution_time.hide()

        self.Button_select_video.show()
        self.Button_start_analyze.show()
        self.label_select_video.show()
        self.Button_start_analyze.setEnabled(False)
        self.Button_start_analyze.setStyleSheet(u"QPushButton{\n"
"	border-radius: 40px;\n"
"	background-color: rgb(166, 166, 166);\n"
" 	font:  20pt \u5fae\u8edf\u6b63\u9ed1\u9ad4;\n"
"}")    
        self.label_select_video.setText("選擇影片")

    def update_progress(self):
        if int(self.progressBar.value()) >= 80:
            self.progress_timer.stop()
        else:
            self.progressBar.setValue(self.progressBar.value() + 1)
    
    def update_execution_time(self):
        elapsed_time = datetime.now() - self.start_time
        minutes, seconds = divmod(elapsed_time.total_seconds(), 60)
        if minutes > 0:
            time_text = f"執行時間: {int(minutes)} 分 {int(seconds)} 秒"
        else:
            time_text = f"執行時間: {int(seconds)} 秒"
        self.label_show_execution_time.setText(time_text)
    
                  
    def analysis_finished(self):
       
        self.progressBar.setValue(100)
        print("Analysis End!")
        
    # mouse event
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False