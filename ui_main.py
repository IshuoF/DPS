# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1440, 960)
        MainWindow.setMaximumSize(QSize(1440, 960))
        MainWindow.setStyleSheet(u"background-color: rgb(98, 116, 164);\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.sidemenu_hide = QWidget(self.centralwidget)
        self.sidemenu_hide.setObjectName(u"sidemenu_hide")
        self.sidemenu_hide.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(98, 116, 164);\n"
"}\n"
"\n"
"QPushButton{\n"
"	color:white;\n"
"	height:70px;\n"
"	border:none;\n"
"	border-radius:10px;\n"
"	padding-right:5px;\n"
"	padding-left:5px;\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	\n"
"	background-color: rgb(86, 99, 136);\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.sidemenu_hide)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, 9, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(50)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 50, 0, -1)
        self.home_hide = QPushButton(self.sidemenu_hide)
        self.home_hide.setObjectName(u"home_hide")
        icon = QIcon()
        icon.addFile(u":/\u65b0\u524d\u7f6e\u5b57\u4e32/images/home-white.png", QSize(), QIcon.Normal, QIcon.Off)
        self.home_hide.setIcon(icon)
        self.home_hide.setIconSize(QSize(50, 50))
        self.home_hide.setCheckable(True)
        self.home_hide.setChecked(True)
        self.home_hide.setAutoExclusive(True)
        self.home_hide.setAutoDefault(False)

        self.verticalLayout.addWidget(self.home_hide)

        self.platform_hide = QPushButton(self.sidemenu_hide)
        self.platform_hide.setObjectName(u"platform_hide")
        icon1 = QIcon()
        icon1.addFile(u":/\u65b0\u524d\u7f6e\u5b57\u4e32/images/platform-white.png", QSize(), QIcon.Normal, QIcon.Off)
        self.platform_hide.setIcon(icon1)
        self.platform_hide.setIconSize(QSize(50, 50))
        self.platform_hide.setCheckable(True)
        self.platform_hide.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.platform_hide)

        self.history_hide = QPushButton(self.sidemenu_hide)
        self.history_hide.setObjectName(u"history_hide")
        icon2 = QIcon()
        icon2.addFile(u":/\u65b0\u524d\u7f6e\u5b57\u4e32/images/history-white.png", QSize(), QIcon.Normal, QIcon.Off)
        self.history_hide.setIcon(icon2)
        self.history_hide.setIconSize(QSize(50, 50))
        self.history_hide.setCheckable(True)
        self.history_hide.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.history_hide)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(20, 416, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.info_hide = QPushButton(self.sidemenu_hide)
        self.info_hide.setObjectName(u"info_hide")
        icon3 = QIcon()
        icon3.addFile(u":/\u65b0\u524d\u7f6e\u5b57\u4e32/images/info-white.png", QSize(), QIcon.Normal, QIcon.Off)
        self.info_hide.setIcon(icon3)
        self.info_hide.setIconSize(QSize(50, 50))
        self.info_hide.setCheckable(True)
        self.info_hide.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.info_hide)


        self.gridLayout.addWidget(self.sidemenu_hide, 1, 0, 1, 1)

        self.sidemenu_visible = QWidget(self.centralwidget)
        self.sidemenu_visible.setObjectName(u"sidemenu_visible")
        self.sidemenu_visible.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(98, 116, 164);\n"
"}\n"
"\n"
"QPushButton{\n"
"	color:white;\n"
"	text-align:left;\n"
"	height:70px;\n"
"	border:none;\n"
"	padding-left:10px;\n"
"	padding-right:20px;\n"
"	border-radius:10px;\n"
"	\n"
"	font: 700 20pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";\n"
"}\n"
"\n"
"QPushButton::contents {\n"
"	padding-left:30px;\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	\n"
"	background-color: rgb(86, 99, 136);\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.sidemenu_visible)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(50)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(20, 50, -1, -1)
        self.home_vis = QPushButton(self.sidemenu_visible)
        self.home_vis.setObjectName(u"home_vis")
        self.home_vis.setIcon(icon)
        self.home_vis.setIconSize(QSize(50, 50))
        self.home_vis.setCheckable(True)
        self.home_vis.setChecked(True)
        self.home_vis.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.home_vis)

        self.platform_vis = QPushButton(self.sidemenu_visible)
        self.platform_vis.setObjectName(u"platform_vis")
        self.platform_vis.setIcon(icon1)
        self.platform_vis.setIconSize(QSize(50, 50))
        self.platform_vis.setCheckable(True)
        self.platform_vis.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.platform_vis)

        self.history_vis = QPushButton(self.sidemenu_visible)
        self.history_vis.setObjectName(u"history_vis")
        self.history_vis.setIcon(icon2)
        self.history_vis.setIconSize(QSize(50, 50))
        self.history_vis.setCheckable(True)
        self.history_vis.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.history_vis)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 408, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.info_vis = QPushButton(self.sidemenu_visible)
        self.info_vis.setObjectName(u"info_vis")
        self.info_vis.setStyleSheet(u"QPushButton {\n"
" 	padding-left: 30px; \n"
"}\n"
"\n"
"")
        self.info_vis.setIcon(icon3)
        self.info_vis.setIconSize(QSize(50, 50))
        self.info_vis.setCheckable(True)
        self.info_vis.setAutoExclusive(True)

        self.verticalLayout_4.addWidget(self.info_vis)


        self.gridLayout.addWidget(self.sidemenu_visible, 1, 1, 1, 1)

        self.Main_content = QWidget(self.centralwidget)
        self.Main_content.setObjectName(u"Main_content")
        self.Main_content.setStyleSheet(u"background-color: rgb(248,248,242);")
        self.verticalLayout_5 = QVBoxLayout(self.Main_content)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.sidebar = QPushButton(self.Main_content)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setStyleSheet(u"border:none;")
        icon4 = QIcon()
        icon4.addFile(u":/\u65b0\u524d\u7f6e\u5b57\u4e32/images/Menubar.png", QSize(), QIcon.Normal, QIcon.Off)
        self.sidebar.setIcon(icon4)
        self.sidebar.setIconSize(QSize(50, 50))
        self.sidebar.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.sidebar)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.stackedWidget = QStackedWidget(self.Main_content)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background-color: rgb(248,248,242);")
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        self.home_page.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"\n"
"}")
        self.label_3 = QLabel(self.home_page)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(430, 40, 281, 151))
        self.label_3.setStyleSheet(u"font: 700 48pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")
        self.pushButton_3 = QPushButton(self.home_page)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(200, 670, 200, 80))
        icon5 = QIcon()
        icon5.addFile(u":/\u65b0\u524d\u7f6e\u5b57\u4e32/images/info.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon5)
        self.pushButton_3.setIconSize(QSize(80, 80))
        self.pushButton_4 = QPushButton(self.home_page)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(200, 545, 200, 80))
        icon6 = QIcon()
        icon6.addFile(u":/\u65b0\u524d\u7f6e\u5b57\u4e32/images/history.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_4.setIcon(icon6)
        self.pushButton_4.setIconSize(QSize(80, 80))
        self.pushButton_5 = QPushButton(self.home_page)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(210, 410, 200, 91))
        icon7 = QIcon()
        icon7.addFile(u":/\u65b0\u524d\u7f6e\u5b57\u4e32/images/platform.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_5.setIcon(icon7)
        self.pushButton_5.setIconSize(QSize(80, 80))
        self.label_4 = QLabel(self.home_page)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(110, 190, 901, 151))
        self.label_4.setStyleSheet(u"font: 700 48pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")
        self.label_4.setAlignment(Qt.AlignCenter)
        self.layoutWidget = QWidget(self.home_page)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(450, 390, 551, 371))
        self.verticalLayout_7 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 700 28pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")

        self.verticalLayout_7.addWidget(self.label)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 700 28pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")

        self.verticalLayout_7.addWidget(self.label_2)

        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"font: 700 28pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")

        self.verticalLayout_7.addWidget(self.label_6)

        self.stackedWidget.addWidget(self.home_page)
        self.platform_page = QWidget()
        self.platform_page.setObjectName(u"platform_page")
        self.Button_select_video = QPushButton(self.platform_page)
        self.Button_select_video.setObjectName(u"Button_select_video")
        self.Button_select_video.setGeometry(QRect(140, 70, 1001, 361))
        self.Button_select_video.setStyleSheet(u"border:none;\n"
"")
        icon8 = QIcon()
        icon8.addFile(u":/\u65b0\u524d\u7f6e\u5b57\u4e32/images/select_video.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Button_select_video.setIcon(icon8)
        self.Button_select_video.setIconSize(QSize(300, 300))
        self.label_select_video = QLabel(self.platform_page)
        self.label_select_video.setObjectName(u"label_select_video")
        self.label_select_video.setGeometry(QRect(290, 440, 711, 91))
        self.label_select_video.setStyleSheet(u"QLabel{\n"
"	text-align: center;\n"
"	font: 28pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";\n"
"	\n"
"}\n"
"")
        self.label_select_video.setAlignment(Qt.AlignCenter)
        self.Button_start_analyze = QPushButton(self.platform_page)
        self.Button_start_analyze.setObjectName(u"Button_start_analyze")
        self.Button_start_analyze.setGeometry(QRect(500, 610, 300, 80))
        self.Button_start_analyze.setStyleSheet(u"QPushButton{\n"
"	border-radius: 40px;\n"
"	background-color: rgb(166, 166, 166);\n"
" 	font:  20pt \u5fae\u8edf\u6b63\u9ed1\u9ad4;\n"
"}")
        self.label_status = QLabel(self.platform_page)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setGeometry(QRect(460, 70, 371, 131))
        self.label_status.setStyleSheet(u"font: 40pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")
        self.label_status.setAlignment(Qt.AlignCenter)
        self.progressBar = QProgressBar(self.platform_page)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(270, 230, 731, 271))
        self.progressBar.setStyleSheet(u"QProgressBar{\n"
"	border : 3px  solid #000000;\n"
"	background : transparent;\n"
"	text-align : center;\n"
"	color : rgb(255,255,255);\n"
" }\n"
"QProgressBar::chunk{\n"
"	background-color :rgb(0,0,0);\n"
"    width: 29.5px;\n"
"    margin: 0.5px;\n"
" }")
        self.progressBar.setValue(24)
        self.label_visual_predict = QLabel(self.platform_page)
        self.label_visual_predict.setObjectName(u"label_visual_predict")
        self.label_visual_predict.setGeometry(QRect(170, 60, 950, 101))
        self.label_visual_predict.setStyleSheet(u"font: 700 36pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")
        self.label_mfcc_predict = QLabel(self.platform_page)
        self.label_mfcc_predict.setObjectName(u"label_mfcc_predict")
        self.label_mfcc_predict.setGeometry(QRect(170, 180, 950, 101))
        self.label_mfcc_predict.setStyleSheet(u"font: 700 36pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")
        self.label_origin_CDR = QLabel(self.platform_page)
        self.label_origin_CDR.setObjectName(u"label_origin_CDR")
        self.label_origin_CDR.setGeometry(QRect(170, 290, 950, 101))
        self.label_origin_CDR.setStyleSheet(u"font: 700 28pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")
        self.label_show_save = QLabel(self.platform_page)
        self.label_show_save.setObjectName(u"label_show_save")
        self.label_show_save.setGeometry(QRect(250, 630, 791, 101))
        self.label_show_save.setStyleSheet(u"font: 700 36pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")
        self.label_show_save.setAlignment(Qt.AlignCenter)
        self.Button_restart = QPushButton(self.platform_page)
        self.Button_restart.setObjectName(u"Button_restart")
        self.Button_restart.setGeometry(QRect(490, 520, 300, 80))
        self.Button_restart.setStyleSheet(u"QPushButton{\n"
"	border-radius: 40px;\n"
"	background-color:  rgb(255, 209, 41);\n"
" 	font:  20pt \u5fae\u8edf\u6b63\u9ed1\u9ad4;\n"
"}")
        self.label_show_execution_time = QLabel(self.platform_page)
        self.label_show_execution_time.setObjectName(u"label_show_execution_time")
        self.label_show_execution_time.setGeometry(QRect(250, 530, 791, 101))
        self.label_show_execution_time.setStyleSheet(u"font:  36pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")
        self.label_show_execution_time.setAlignment(Qt.AlignCenter)
        self.label_show_final_execution_time = QLabel(self.platform_page)
        self.label_show_final_execution_time.setObjectName(u"label_show_final_execution_time")
        self.label_show_final_execution_time.setGeometry(QRect(250, 410, 791, 101))
        self.label_show_final_execution_time.setStyleSheet(u"font: 700 20pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")
        self.label_show_final_execution_time.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(self.platform_page)
        self.history_page = QWidget()
        self.history_page.setObjectName(u"history_page")
        self.label_5 = QLabel(self.history_page)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(70, 50, 151, 61))
        self.label_5.setStyleSheet(u"font: 700 26pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")
        self.history_table = QTableWidget(self.history_page)
        if (self.history_table.columnCount() < 5):
            self.history_table.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.history_table.setObjectName(u"history_table")
        self.history_table.setGeometry(QRect(70, 210, 1002, 431))
        self.history_table.setStyleSheet(u"font: 700 12pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")
        self.history_table.setLineWidth(1)
        self.history_table.setRowCount(0)
        self.history_table.setColumnCount(5)
        self.history_table.horizontalHeader().setMinimumSectionSize(30)
        self.history_table.horizontalHeader().setDefaultSectionSize(200)
        self.history_table.verticalHeader().setDefaultSectionSize(30)
        self.button_search_history = QPushButton(self.history_page)
        self.button_search_history.setObjectName(u"button_search_history")
        self.button_search_history.setGeometry(QRect(250, 65, 131, 41))
        self.button_search_history.setStyleSheet(u"font: 20pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";\n"
"background-color:rgb(98, 116, 164);\n"
"color:white;\n"
"border-radius:10px")
        self.stackedWidget.addWidget(self.history_page)
        self.info_page = QWidget()
        self.info_page.setObjectName(u"info_page")
        self.label_8 = QLabel(self.info_page)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(290, 60, 591, 251))
        self.label_8.setStyleSheet(u"font: 700 48pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";")
        self.stackedWidget.addWidget(self.info_page)

        self.verticalLayout_5.addWidget(self.stackedWidget)


        self.gridLayout.addWidget(self.Main_content, 1, 2, 1, 1)

        self.title_bar = QWidget(self.centralwidget)
        self.title_bar.setObjectName(u"title_bar")
        self.title_bar.setMinimumSize(QSize(1440, 80))
        self.title_bar.setMaximumSize(QSize(1440, 60))
        self.title_bar.setStyleSheet(u"background-color: rgb(98,116,164);\n"
"\n"
"                                                                                                                                                                                                                                                                ")
        self.layoutWidget1 = QWidget(self.title_bar)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(11, 4, 607, 61))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 0, 0)
        self.logo = QLabel(self.layoutWidget1)
        self.logo.setObjectName(u"logo")
        self.logo.setMaximumSize(QSize(100000, 100000))
        self.logo.setPixmap(QPixmap(u":/\u65b0\u524d\u7f6e\u5b57\u4e32/images/375259_bed_hospital_patient_icon.png"))

        self.horizontalLayout.addWidget(self.logo)

        self.title = QLabel(self.layoutWidget1)
        self.title.setObjectName(u"title")
        self.title.setStyleSheet(u"QLabel{\n"
"	color:white;\n"
"	padding-left:10px;\n"
"	\n"
"	font: 700 28pt \"\u5fae\u8edf\u6b63\u9ed1\u9ad4\";\n"
"	\n"
"}")

        self.horizontalLayout.addWidget(self.title)

        self.layoutWidget2 = QWidget(self.title_bar)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(1280, 10, 164, 60))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 5, 0, 5)
        self.minimum_button = QPushButton(self.layoutWidget2)
        self.minimum_button.setObjectName(u"minimum_button")
        self.minimum_button.setMinimumSize(QSize(50, 50))
        self.minimum_button.setMaximumSize(QSize(50, 50))
        self.minimum_button.setStyleSheet(u"border:none;")
        icon9 = QIcon()
        icon9.addFile(u":/\u65b0\u524d\u7f6e\u5b57\u4e32/images/minimum-white.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimum_button.setIcon(icon9)
        self.minimum_button.setIconSize(QSize(50, 50))
        self.minimum_button.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.minimum_button)

        self.close_button = QPushButton(self.layoutWidget2)
        self.close_button.setObjectName(u"close_button")
        self.close_button.setMinimumSize(QSize(50, 50))
        self.close_button.setMaximumSize(QSize(50, 50))
        self.close_button.setStyleSheet(u"border:none;")
        icon10 = QIcon()
        icon10.addFile(u":/\u65b0\u524d\u7f6e\u5b57\u4e32/images/close-white.png", QSize(), QIcon.Normal, QIcon.Off)
        self.close_button.setIcon(icon10)
        self.close_button.setIconSize(QSize(50, 50))
        self.close_button.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.close_button)


        self.gridLayout.addWidget(self.title_bar, 0, 0, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.sidebar.toggled.connect(self.sidemenu_hide.setHidden)
        self.sidebar.toggled.connect(self.sidemenu_visible.setVisible)
        self.history_hide.toggled.connect(self.history_vis.setChecked)
        self.platform_hide.toggled.connect(self.platform_vis.setChecked)
        self.home_hide.toggled.connect(self.home_vis.setChecked)
        self.home_vis.toggled.connect(self.home_hide.setChecked)
        self.platform_vis.toggled.connect(self.platform_hide.setChecked)
        self.history_vis.toggled.connect(self.history_hide.setChecked)
        self.info_hide.toggled.connect(self.info_vis.setChecked)
        self.info_vis.toggled.connect(self.info_hide.setChecked)
        self.minimum_button.clicked["bool"].connect(MainWindow.showMinimized)
        self.close_button.clicked["bool"].connect(MainWindow.close)

        self.stackedWidget.setCurrentIndex(0)
        self.progressBar.hide()
        self.label_status.hide()
        self.label_visual_predict.hide()
        self.label_mfcc_predict.hide()
        self.label_origin_CDR.hide()
        self.label_show_save.hide()
        self.label_show_execution_time.hide()
        self.label_show_final_execution_time.hide()
        self.Button_restart.hide()
        self.progressBar.setTextVisible(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.home_hide.setText("")
        self.platform_hide.setText("")
        self.history_hide.setText("")
        self.info_hide.setText("")
        self.home_vis.setText(QCoreApplication.translate("MainWindow", u"\u9996\u9801", None))
        self.platform_vis.setText(QCoreApplication.translate("MainWindow", u"\u6aa2\u6e2c\u5e73\u53f0", None))
        self.history_vis.setText(QCoreApplication.translate("MainWindow", u"\u6b77\u53f2\u7d00\u9304", None))
        self.info_vis.setText(QCoreApplication.translate("MainWindow", u"\u8cc7\u8a0a\u670d\u52d9", None))
        self.sidebar.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u6b61\u8fce\u4f7f\u7528", None))
        self.pushButton_3.setText("")
        self.pushButton_4.setText("")
        self.pushButton_5.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u5931\u667a\u75c7\u6aa2\u6e2c\u7cfb\u7d71", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u9032\u5165\u6aa2\u6e2c\u5e73\u53f0\uff0c\u9032\u884c\u6aa2\u6e2c", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8a62\u6b77\u53f2\u6aa2\u6e2c\u7d00\u9304", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u5982\u6709\u6280\u8853\u554f\u984c\uff0c\u8acb\u9ede\u9078\u8cc7\u8a0a\u670d\u52d9", None))
        self.Button_select_video.setText("")
        self.label_select_video.setText(QCoreApplication.translate("MainWindow", u"\u9078\u64c7\u5f71\u7247", None))
        self.Button_start_analyze.setText(QCoreApplication.translate("MainWindow", u"\u958b\u59cb\u5206\u6790", None))
        self.label_status.setText(QCoreApplication.translate("MainWindow", u"\u76ee\u524d\u72c0\u614b", None))
        self.label_visual_predict.setText("")
        self.label_mfcc_predict.setText("")
        self.label_origin_CDR.setText("")
        self.label_show_save.setText("")
        self.Button_restart.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u65b0\u6aa2\u6e2c", None))
        self.label_show_execution_time.setText("")
        self.label_show_final_execution_time.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u6aa2\u6e2c\u7d00\u9304", None))
        ___qtablewidgetitem = self.history_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u75c5\u4eba\u540d\u7a31", None));
        ___qtablewidgetitem1 = self.history_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"CDR", None));
        ___qtablewidgetitem2 = self.history_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u8996\u8a0a\u8a55\u4f30CDR", None));
        ___qtablewidgetitem3 = self.history_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u8a0a\u8a55\u4f30CDR", None));
        ___qtablewidgetitem4 = self.history_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u8a55\u4f30\u65e5\u671f", None));
        self.button_search_history.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8a62", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"NCKU MMCVLab", None))
        self.logo.setText("")
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u57fa\u65bc\u8996\u8a0a\u8207\u97f3\u8a0a\u5931\u667a\u75c7\u6aa2\u6e2c\u7cfb\u7d71", None))
        self.minimum_button.setText("")
        self.close_button.setText("")
    # retranslateUi

