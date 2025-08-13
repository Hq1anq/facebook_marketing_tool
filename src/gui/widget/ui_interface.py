# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfaceyUQOiE.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtGui import QCursor, QFont, QIcon, QPixmap
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QPlainTextEdit,
    QPushButton, QScrollArea, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget)

from src.gui.custom_widget.highlighted_widget import HighlightLabel, HighlightPlainTextEdit

import resources.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1005, 700)
        MainWindow.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        self.styleSheet.setEnabled(True)
        self.styleSheet.setStyleSheet(u"*{ border: none }\n"
"#navigationBar .QPushButton { height: 44px; width: 44px }\n"
"#navigationBar .QPushButton:hover {\n"
"	background-color: rgb(44, 49, 57);\n"
"	border-style: solid; border-radius: 4px }\n"
"#navigationBar .QPushButton:pressed {\n"
"	background-color: rgb(23, 26, 30);\n"
"	border-style: solid;\n"
"	border-radius: 4px }\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\" }\n"
"QLabel, QPushButton, QLineEdit, QComboBox, QCheckBox, QTextEdit, QPlainTextEdit {\n"
"	font-size: 20px }\n"
"QPushButton {font-weight: bold}\n"
"QComboBox{\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px }\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88) }\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom"
                        "-right-radius: 3px;\n"
"	background-image: url(:/icons/icons/arrowDown.svg);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54) }\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60) }\n"
"QCheckBox::indicator:hover { border: 3px solid rgb(58, 66, 81) }\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);\n"
"	background-image: url(:/icons/icons/check.svg) }\n"
"QTableCornerButton::section { background-color: rgb(33, 37, 43) }\n"
"QTableWidget {	\n"
"	padding: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"	font-size: 10px }\n"
"QTableWidget::item{ border-color: rgb(44, 49, 60) }\n"
"QTable"
                        "Widget::item:selected{ background-color: rgb(189, 147, 249) }\n"
"QHeaderView { qproperty-defaultAlignment: AlignCenter }\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	font-size: 15px }\n"
"QScrollBar:horizontal {\n"
"	border: none;\n"
"	background: rgb(52, 59, 72);\n"
"	height: 8px;\n"
"	margin: 0px 21px 0 21px;\n"
"	border-radius: 0px }\n"
"QScrollBar::handle:horizontal {\n"
"	background: rgb(189, 147, 249);\n"
"	min-width: 25px;\n"
"	border-radius: 4px }\n"
"QScrollBar::handle:horizontal:hover, QScrollBar::handle:vertical:hover {\n"
"	background: rgb(208, 181, 249) }\n"
"QScrollBar::handle:horizontal:pressed, QScrollBar::handle:vertical:pressed {\n"
"	background: rgb(161, 103, 249) }\n"
"QScrollBar::add-line:horizontal {\n"
"	border: none;\n"
"	background: rgb(55, 63, 77);\n"
"	width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"	border-bottom-right-radius: 4px;\n"
"	subcontrol-position: right;\n"
"	subcontrol-origin: margin }\n"
"QScrollBar::"
                        "sub-line:horizontal {\n"
"	border: none;\n"
"	background: rgb(55, 63, 77);\n"
"	width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"	border-bottom-left-radius: 4px;\n"
"	subcontrol-position: left;\n"
"	subcontrol-origin: margin }\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal,\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal,\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"	background: none }\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px }\n"
"QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"	min-height: 25px;\n"
"	border-radius: 4px }\n"
"QScrollBar::add-line:vertical {\n"
"	border: none;\n"
"	background: rgb(55, 63, 77);\n"
"	height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"	border-bottom-right-radius: 4px;\n"
"	subcontrol-position: botto"
                        "m;\n"
"	subcontrol-origin: margin }\n"
"QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"	background: rgb(55, 63, 77);\n"
"	height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"	border-top-right-radius: 4px;\n"
"	subcontrol-position: top;\n"
"	subcontrol-origin: margin }\n"
"QScrollBar::add-line:horizontal:hover, QScrollBar::sub-line:horizontal:hover,\n"
"QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {\n"
"	background: rgb(64, 69, 77) }\n"
"QScrollBar::add-line:horizontal:pressed, QScrollBar::sub-line:horizontal:pressed,\n"
"QScrollBar::add-line:vertical:pressed, QScrollBar::sub-line:vertical:pressed {\n"
"	background: rgb(189, 147, 249) }")
        self.gridLayout_3 = QGridLayout(self.styleSheet)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.App = QWidget(self.styleSheet)
        self.App.setObjectName(u"App")
        self.App.setStyleSheet(u"#App { background-color: #2C313A }\n"
"#title {font-size: 20px; font-weight: bold}\n"
"#leftMenu {background-color: rgb(33, 37, 43); border: none }\n"
"	#leftMenuBtn .QPushButton {\n"
"		padding-left: 14px;\n"
"		text-align: left;\n"
"		border: none }\n"
"	#leftMenuBtn .QPushButton:hover, #btn_toggle:hover {\n"
"		background-color: rgb(40, 44, 52) }\n"
"	#leftMenuBtn .QPushButton:pressed, #btn_toggle:pressed {	\n"
"		background-color: rgb(189, 147, 249);\n"
"		color: rgb(255, 255, 255) }\n"
"	#btn_toggle { background-color: rgb(37, 41, 48) }\n"
"	#btn_proxy { padding-top: 5px; padding-bottom: 5px }\n"
"#contentTop { background-color: rgb(33, 37, 43) }\n"
"#bottomBar QPushButton {\n"
"	font-size: 11px; color: rgb(113, 126, 149);\n"
"	padding-left: 2px; padding-bottom: 2px }\n"
"#profileName { font-size: 15px }")
        self._14 = QGridLayout(self.App)
        self._14.setObjectName(u"_14")
        self._14.setHorizontalSpacing(0)
        self._14.setVerticalSpacing(3)
        self._14.setContentsMargins(0, 0, 0, 0)
        self.leftMenu = QFrame(self.App)
        self.leftMenu.setObjectName(u"leftMenu")
        self.leftMenu.setMinimumSize(QSize(60, 0))
        self.leftMenu.setMaximumSize(QSize(60, 16777215))
        self._19 = QVBoxLayout(self.leftMenu)
        self._19.setSpacing(0)
        self._19.setObjectName(u"_19")
        self._19.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBtn = QFrame(self.leftMenu)
        self.leftMenuBtn.setObjectName(u"leftMenuBtn")
        self.leftMenuBtn.setMinimumSize(QSize(60, 0))
        self._8 = QVBoxLayout(self.leftMenuBtn)
        self._8.setSpacing(0)
        self._8.setObjectName(u"_8")
        self._8.setContentsMargins(0, 0, 0, 0)
        self.btn_toggle = QPushButton(self.leftMenuBtn)
        self.btn_toggle.setObjectName(u"btn_toggle")
        self.btn_toggle.setMinimumSize(QSize(60, 45))
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/menu.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_toggle.setIcon(icon1)
        self.btn_toggle.setIconSize(QSize(32, 32))

        self._8.addWidget(self.btn_toggle)

        self.btn_home = QPushButton(self.leftMenuBtn)
        self.btn_home.setObjectName(u"btn_home")
        self.btn_home.setMinimumSize(QSize(60, 45))
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/home.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_home.setIcon(icon2)
        self.btn_home.setIconSize(QSize(32, 32))

        self._8.addWidget(self.btn_home)

        self.btn_get = QPushButton(self.leftMenuBtn)
        self.btn_get.setObjectName(u"btn_get")
        self.btn_get.setMinimumSize(QSize(60, 45))
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/recive.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_get.setIcon(icon3)
        self.btn_get.setIconSize(QSize(32, 32))

        self._8.addWidget(self.btn_get)

        self.btn_proxy = QPushButton(self.leftMenuBtn)
        self.btn_proxy.setObjectName(u"btn_proxy")
        self.btn_proxy.setMinimumSize(QSize(60, 45))
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/proxyUnCheckBox.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon4.addFile(u":/icons/icons/proxyCheckBox.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.btn_proxy.setIcon(icon4)
        self.btn_proxy.setIconSize(QSize(32, 55))
        self.btn_proxy.setCheckable(True)

        self._8.addWidget(self.btn_proxy)

        self.btn_save = QPushButton(self.leftMenuBtn)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setMinimumSize(QSize(60, 45))
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/save.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_save.setIcon(icon5)
        self.btn_save.setIconSize(QSize(32, 32))

        self._8.addWidget(self.btn_save)


        self._19.addWidget(self.leftMenuBtn, 0, Qt.AlignmentFlag.AlignTop)


        self._14.addWidget(self.leftMenu, 1, 0, 1, 1)

        self.pageContainer = QFrame(self.App)
        self.pageContainer.setObjectName(u"pageContainer")
        self.pageContainer.setMinimumSize(QSize(50, 0))
        self.pageContainer.setStyleSheet(u"background-color: rgb(40, 44, 52)")
        self.vboxLayout = QVBoxLayout(self.pageContainer)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.vboxLayout.setContentsMargins(0, -1, 0, 0)
        self.pageStacked = QStackedWidget(self.pageContainer)
        self.pageStacked.setObjectName(u"pageStacked")
        self.pageStacked.setStyleSheet(u"QPushButton {\n"
"	border: 3px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"	padding: 10px }\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 3px solid rgb(61, 70, 86) }\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 3px solid rgb(43, 50, 61) }\n"
"QLabel { qproperty-alignment: AlignCenter }\n"
"QLineEdit, QTextEdit, QPlainTextEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 3px;\n"
"	selection-background-color: rgb(255, 121, 198);\n"
" 	selection-color: rgb(40, 44, 52) }\n"
"QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover { border: 2px solid rgb(64, 71, 88) }\n"
"QLineEdit:focus,  QTextEdit:focus, QPlainTextEdit:hover { border: 2px solid rgb(91, 101, 124) }\n"
"QComboBox { background-color: rgb(33, 37, 43) }\n"
"#btn_ok { padding: 30px }")
        self.homePage = QWidget()
        self.homePage.setObjectName(u"homePage")
        self.gridLayout_8 = QGridLayout(self.homePage)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(15)
        self.gridLayout_8.setVerticalSpacing(0)
        self.statusHome = HighlightLabel(self.homePage)
        self.statusHome.setObjectName(u"statusHome")

        self.gridLayout_8.addWidget(self.statusHome, 1, 0, 1, 3)

        self.functionComboBox = QComboBox(self.homePage)
        self.functionComboBox.addItem("")
        self.functionComboBox.addItem("")
        self.functionComboBox.addItem("")
        self.functionComboBox.setObjectName(u"functionComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.functionComboBox.sizePolicy().hasHeightForWidth())
        self.functionComboBox.setSizePolicy(sizePolicy)
        self.functionComboBox.setStyleSheet(u"")
        self.functionComboBox.setIconSize(QSize(20, 20))

        self.gridLayout_8.addWidget(self.functionComboBox, 0, 0, 1, 1)

        self.btn_homeReload = QPushButton(self.homePage)
        self.btn_homeReload.setObjectName(u"btn_homeReload")
        self.btn_homeReload.setMaximumSize(QSize(43, 43))
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/update.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_homeReload.setIcon(icon6)
        self.btn_homeReload.setIconSize(QSize(30, 30))

        self.gridLayout_8.addWidget(self.btn_homeReload, 0, 1, 1, 1)

        self.homeStackedWidget = QStackedWidget(self.homePage)
        self.homeStackedWidget.setObjectName(u"homeStackedWidget")
        self.postPage = QWidget()
        self.postPage.setObjectName(u"postPage")
        self.formLayout_2 = QFormLayout(self.postPage)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(80)
        self.postDelay = QFrame(self.postPage)
        self.postDelay.setObjectName(u"postDelay")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.postDelay.sizePolicy().hasHeightForWidth())
        self.postDelay.setSizePolicy(sizePolicy1)
        self.postDelay.setFrameShape(QFrame.Shape.StyledPanel)
        self.postDelay.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.postDelay)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(30, -1, -1, -1)
        self.postDelayLabel = QLabel(self.postDelay)
        self.postDelayLabel.setObjectName(u"postDelayLabel")

        self.horizontalLayout.addWidget(self.postDelayLabel)

        self.postDelayInput = QLineEdit(self.postDelay)
        self.postDelayInput.setObjectName(u"postDelayInput")

        self.horizontalLayout.addWidget(self.postDelayInput)


        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.postDelay)

        self.btn_post = QPushButton(self.postPage)
        self.btn_post.setObjectName(u"btn_post")
        sizePolicy.setHeightForWidth(self.btn_post.sizePolicy().hasHeightForWidth())
        self.btn_post.setSizePolicy(sizePolicy)
        icon7 = QIcon()
        icon7.addFile(u":/icons/icons/post.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_post.setIcon(icon7)
        self.btn_post.setIconSize(QSize(50, 40))

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.btn_post)

        self.postInputImageContent = QFrame(self.postPage)
        self.postInputImageContent.setObjectName(u"postInputImageContent")
        self.postInputImageContent.setFrameShape(QFrame.Shape.StyledPanel)
        self.postInputImageContent.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.postInputImageContent)
        self.gridLayout.setObjectName(u"gridLayout")
        self.postImageViewer = QScrollArea(self.postInputImageContent)
        self.postImageViewer.setObjectName(u"postImageViewer")
        self.postImageViewer.setStyleSheet(u"background-color: rgb(33, 37, 43)")
        self.postImageViewer.setWidgetResizable(True)
        self.postImageViewer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.postImageViewerWidget = QWidget()
        self.postImageViewerWidget.setObjectName(u"postImageViewerWidget")
        self.postImageViewerWidget.setGeometry(QRect(0, 0, 100, 30))
        self.postImageViewer.setWidget(self.postImageViewerWidget)

        self.gridLayout.addWidget(self.postImageViewer, 2, 0, 1, 1)

        self.postContentCheckBox = QCheckBox(self.postInputImageContent)
        self.postContentCheckBox.setObjectName(u"postContentCheckBox")
        sizePolicy.setHeightForWidth(self.postContentCheckBox.sizePolicy().hasHeightForWidth())
        self.postContentCheckBox.setSizePolicy(sizePolicy)
        self.postContentCheckBox.setChecked(True)

        self.gridLayout.addWidget(self.postContentCheckBox, 1, 2, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.upImageCheckBoxFrame = QFrame(self.postInputImageContent)
        self.upImageCheckBoxFrame.setObjectName(u"upImageCheckBoxFrame")
        sizePolicy1.setHeightForWidth(self.upImageCheckBoxFrame.sizePolicy().hasHeightForWidth())
        self.upImageCheckBoxFrame.setSizePolicy(sizePolicy1)
        self.upImageCheckBoxFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.upImageCheckBoxFrame.setFrameShadow(QFrame.Shadow.Raised)
        self._9 = QHBoxLayout(self.upImageCheckBoxFrame)
        self._9.setObjectName(u"_9")
        self._9.setContentsMargins(-1, 0, -1, 0)
        self.postImageCheckBox = QCheckBox(self.upImageCheckBoxFrame)
        self.postImageCheckBox.setObjectName(u"postImageCheckBox")
        sizePolicy.setHeightForWidth(self.postImageCheckBox.sizePolicy().hasHeightForWidth())
        self.postImageCheckBox.setSizePolicy(sizePolicy)
        self.postImageCheckBox.setChecked(True)

        self._9.addWidget(self.postImageCheckBox)

        self.btn_postImageFromFile = QPushButton(self.upImageCheckBoxFrame)
        self.btn_postImageFromFile.setObjectName(u"btn_postImageFromFile")
        self.btn_postImageFromFile.setMaximumSize(QSize(40, 40))
        icon8 = QIcon()
        icon8.addFile(u":/icons/icons/openedFile.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_postImageFromFile.setIcon(icon8)
        self.btn_postImageFromFile.setIconSize(QSize(30, 30))

        self._9.addWidget(self.btn_postImageFromFile)


        self.gridLayout.addWidget(self.upImageCheckBoxFrame, 1, 0, 1, 1)

        self.postContentInput = QPlainTextEdit(self.postInputImageContent)
        self.postContentInput.setObjectName(u"postContentInput")

        self.gridLayout.addWidget(self.postContentInput, 2, 2, 1, 1)


        self.formLayout_2.setWidget(1, QFormLayout.SpanningRole, self.postInputImageContent)

        self.homeStackedWidget.addWidget(self.postPage)
        self.commentPage = QWidget()
        self.commentPage.setObjectName(u"commentPage")
        self.formLayout = QFormLayout(self.commentPage)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(80)
        self.commentDelay = QFrame(self.commentPage)
        self.commentDelay.setObjectName(u"commentDelay")
        self.commentDelay.setMinimumSize(QSize(350, 0))
        self.commentDelay.setFrameShape(QFrame.Shape.StyledPanel)
        self.commentDelay.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.commentDelay)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(30, -1, -1, -1)
        self.commentDelayLabel = QLabel(self.commentDelay)
        self.commentDelayLabel.setObjectName(u"commentDelayLabel")

        self.horizontalLayout_2.addWidget(self.commentDelayLabel)

        self.commentDelayInput = QLineEdit(self.commentDelay)
        self.commentDelayInput.setObjectName(u"commentDelayInput")

        self.horizontalLayout_2.addWidget(self.commentDelayInput)


        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.commentDelay)

        self.commentInputImageContent = QFrame(self.commentPage)
        self.commentInputImageContent.setObjectName(u"commentInputImageContent")
        self.commentInputImageContent.setFrameShape(QFrame.Shape.StyledPanel)
        self.commentInputImageContent.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.commentInputImageContent)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.commentImageViewer = QScrollArea(self.commentInputImageContent)
        self.commentImageViewer.setObjectName(u"commentImageViewer")
        self.commentImageViewer.setStyleSheet(u"background-color: rgb(33, 37, 43)")
        self.commentImageViewer.setWidgetResizable(True)
        self.commentImageViewer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.commentImageViewerWidget = QWidget()
        self.commentImageViewerWidget.setObjectName(u"commentImageViewerWidget")
        self.commentImageViewerWidget.setGeometry(QRect(0, 0, 100, 30))
        self.commentImageViewer.setWidget(self.commentImageViewerWidget)

        self.gridLayout_10.addWidget(self.commentImageViewer, 2, 0, 1, 1)

        self.commentContentCheckBox = QCheckBox(self.commentInputImageContent)
        self.commentContentCheckBox.setObjectName(u"commentContentCheckBox")
        sizePolicy.setHeightForWidth(self.commentContentCheckBox.sizePolicy().hasHeightForWidth())
        self.commentContentCheckBox.setSizePolicy(sizePolicy)
        self.commentContentCheckBox.setChecked(True)

        self.gridLayout_10.addWidget(self.commentContentCheckBox, 1, 2, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.commentImageCheckBoxFrame = QFrame(self.commentInputImageContent)
        self.commentImageCheckBoxFrame.setObjectName(u"commentImageCheckBoxFrame")
        sizePolicy1.setHeightForWidth(self.commentImageCheckBoxFrame.sizePolicy().hasHeightForWidth())
        self.commentImageCheckBoxFrame.setSizePolicy(sizePolicy1)
        self.commentImageCheckBoxFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.commentImageCheckBoxFrame.setFrameShadow(QFrame.Shadow.Raised)
        self._10 = QHBoxLayout(self.commentImageCheckBoxFrame)
        self._10.setObjectName(u"_10")
        self._10.setContentsMargins(-1, 0, -1, 0)
        self.commentImageCheckBox = QCheckBox(self.commentImageCheckBoxFrame)
        self.commentImageCheckBox.setObjectName(u"commentImageCheckBox")
        sizePolicy.setHeightForWidth(self.commentImageCheckBox.sizePolicy().hasHeightForWidth())
        self.commentImageCheckBox.setSizePolicy(sizePolicy)
        self.commentImageCheckBox.setChecked(True)

        self._10.addWidget(self.commentImageCheckBox)

        self.btn_commentImageFromFile = QPushButton(self.commentImageCheckBoxFrame)
        self.btn_commentImageFromFile.setObjectName(u"btn_commentImageFromFile")
        self.btn_commentImageFromFile.setMaximumSize(QSize(40, 40))
        self.btn_commentImageFromFile.setIcon(icon8)
        self.btn_commentImageFromFile.setIconSize(QSize(30, 30))

        self._10.addWidget(self.btn_commentImageFromFile)


        self.gridLayout_10.addWidget(self.commentImageCheckBoxFrame, 1, 0, 1, 1)

        self.commentContentInput = QPlainTextEdit(self.commentInputImageContent)
        self.commentContentInput.setObjectName(u"commentContentInput")

        self.gridLayout_10.addWidget(self.commentContentInput, 2, 2, 1, 1)


        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.commentInputImageContent)

        self.btn_comment = QPushButton(self.commentPage)
        self.btn_comment.setObjectName(u"btn_comment")
        sizePolicy.setHeightForWidth(self.btn_comment.sizePolicy().hasHeightForWidth())
        self.btn_comment.setSizePolicy(sizePolicy)
        self.btn_comment.setMaximumSize(QSize(16777215, 70))
        icon9 = QIcon()
        icon9.addFile(u":/icons/icons/comment.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_comment.setIcon(icon9)
        self.btn_comment.setIconSize(QSize(50, 50))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.btn_comment)

        self.homeStackedWidget.addWidget(self.commentPage)
        self.spamPage = QWidget()
        self.spamPage.setObjectName(u"spamPage")
        self.gridLayout_2 = QGridLayout(self.spamPage)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.spamScrollNumberInput = QLineEdit(self.spamPage)
        self.spamScrollNumberInput.setObjectName(u"spamScrollNumberInput")

        self.gridLayout_2.addWidget(self.spamScrollNumberInput, 0, 2, 1, 2)

        self.spamInputImageContent = QFrame(self.spamPage)
        self.spamInputImageContent.setObjectName(u"spamInputImageContent")
        self.spamInputImageContent.setFrameShape(QFrame.Shape.StyledPanel)
        self.spamInputImageContent.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.spamInputImageContent)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.spamImageViewer = QScrollArea(self.spamInputImageContent)
        self.spamImageViewer.setObjectName(u"spamImageViewer")
        self.spamImageViewer.setStyleSheet(u"background-color: rgb(33, 37, 43)")
        self.spamImageViewer.setWidgetResizable(True)
        self.spamImageViewer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spamImageViewerWidget = QWidget()
        self.spamImageViewerWidget.setObjectName(u"spamImageViewerWidget")
        self.spamImageViewerWidget.setGeometry(QRect(0, 0, 100, 30))
        self.spamImageViewer.setWidget(self.spamImageViewerWidget)

        self.gridLayout_11.addWidget(self.spamImageViewer, 2, 0, 1, 1)

        self.spamContentCheckBox = QCheckBox(self.spamInputImageContent)
        self.spamContentCheckBox.setObjectName(u"spamContentCheckBox")
        sizePolicy.setHeightForWidth(self.spamContentCheckBox.sizePolicy().hasHeightForWidth())
        self.spamContentCheckBox.setSizePolicy(sizePolicy)
        self.spamContentCheckBox.setChecked(True)

        self.gridLayout_11.addWidget(self.spamContentCheckBox, 1, 2, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.spamImageCheckBoxFrame = QFrame(self.spamInputImageContent)
        self.spamImageCheckBoxFrame.setObjectName(u"spamImageCheckBoxFrame")
        sizePolicy1.setHeightForWidth(self.spamImageCheckBoxFrame.sizePolicy().hasHeightForWidth())
        self.spamImageCheckBoxFrame.setSizePolicy(sizePolicy1)
        self.spamImageCheckBoxFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.spamImageCheckBoxFrame.setFrameShadow(QFrame.Shadow.Raised)
        self._12 = QHBoxLayout(self.spamImageCheckBoxFrame)
        self._12.setObjectName(u"_12")
        self._12.setContentsMargins(-1, 0, -1, 0)
        self.spamImageCheckBox = QCheckBox(self.spamImageCheckBoxFrame)
        self.spamImageCheckBox.setObjectName(u"spamImageCheckBox")
        sizePolicy.setHeightForWidth(self.spamImageCheckBox.sizePolicy().hasHeightForWidth())
        self.spamImageCheckBox.setSizePolicy(sizePolicy)
        self.spamImageCheckBox.setChecked(True)

        self._12.addWidget(self.spamImageCheckBox)

        self.btn_spamImageFromFile = QPushButton(self.spamImageCheckBoxFrame)
        self.btn_spamImageFromFile.setObjectName(u"btn_spamImageFromFile")
        self.btn_spamImageFromFile.setMaximumSize(QSize(40, 40))
        self.btn_spamImageFromFile.setIcon(icon8)
        self.btn_spamImageFromFile.setIconSize(QSize(30, 30))

        self._12.addWidget(self.btn_spamImageFromFile)


        self.gridLayout_11.addWidget(self.spamImageCheckBoxFrame, 1, 0, 1, 1)

        self.spamContentInput = QPlainTextEdit(self.spamInputImageContent)
        self.spamContentInput.setObjectName(u"spamContentInput")

        self.gridLayout_11.addWidget(self.spamContentInput, 2, 2, 1, 1)


        self.gridLayout_2.addWidget(self.spamInputImageContent, 4, 0, 1, 13)

        self.spamSpamDelayInput = QLineEdit(self.spamPage)
        self.spamSpamDelayInput.setObjectName(u"spamSpamDelayInput")
        sizePolicy.setHeightForWidth(self.spamSpamDelayInput.sizePolicy().hasHeightForWidth())
        self.spamSpamDelayInput.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.spamSpamDelayInput, 1, 2, 1, 2)

        self.spamSpamDelay = QLabel(self.spamPage)
        self.spamSpamDelay.setObjectName(u"spamSpamDelay")

        self.gridLayout_2.addWidget(self.spamSpamDelay, 1, 0, 1, 2)

        self.spamPostNumber = QLabel(self.spamPage)
        self.spamPostNumber.setObjectName(u"spamPostNumber")

        self.gridLayout_2.addWidget(self.spamPostNumber, 0, 4, 1, 1)

        self.spamScanDelayInput = QLineEdit(self.spamPage)
        self.spamScanDelayInput.setObjectName(u"spamScanDelayInput")
        sizePolicy.setHeightForWidth(self.spamScanDelayInput.sizePolicy().hasHeightForWidth())
        self.spamScanDelayInput.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.spamScanDelayInput, 1, 5, 1, 1)

        self.spamScrollNumber = QLabel(self.spamPage)
        self.spamScrollNumber.setObjectName(u"spamScrollNumber")
        sizePolicy1.setHeightForWidth(self.spamScrollNumber.sizePolicy().hasHeightForWidth())
        self.spamScrollNumber.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.spamScrollNumber, 0, 0, 1, 2)

        self.spamScanDelay = QLabel(self.spamPage)
        self.spamScanDelay.setObjectName(u"spamScanDelay")

        self.gridLayout_2.addWidget(self.spamScanDelay, 1, 4, 1, 1)

        self.spamPostNumberInput = QLineEdit(self.spamPage)
        self.spamPostNumberInput.setObjectName(u"spamPostNumberInput")
        sizePolicy.setHeightForWidth(self.spamPostNumberInput.sizePolicy().hasHeightForWidth())
        self.spamPostNumberInput.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.spamPostNumberInput, 0, 5, 1, 1)

        self.btn_spam = QPushButton(self.spamPage)
        self.btn_spam.setObjectName(u"btn_spam")

        self.gridLayout_2.addWidget(self.btn_spam, 0, 7, 4, 5)

        self.spamListFilter = QLineEdit(self.spamPage)
        self.spamListFilter.setObjectName(u"spamListFilter")

        self.gridLayout_2.addWidget(self.spamListFilter, 2, 2, 1, 4)

        self.spamSpamListFilter = QCheckBox(self.spamPage)
        self.spamSpamListFilter.setObjectName(u"spamSpamListFilter")
        sizePolicy.setHeightForWidth(self.spamSpamListFilter.sizePolicy().hasHeightForWidth())
        self.spamSpamListFilter.setSizePolicy(sizePolicy)
        self.spamSpamListFilter.setChecked(True)

        self.gridLayout_2.addWidget(self.spamSpamListFilter, 2, 0, 1, 2, Qt.AlignmentFlag.AlignRight)

        self.homeStackedWidget.addWidget(self.spamPage)

        self.gridLayout_8.addWidget(self.homeStackedWidget, 2, 0, 1, 3)

        self.pageStacked.addWidget(self.homePage)
        self.proxyPage = QWidget()
        self.proxyPage.setObjectName(u"proxyPage")
        self.proxyLayout = QGridLayout(self.proxyPage)
        self.proxyLayout.setObjectName(u"proxyLayout")
        self.proxyLayout.setVerticalSpacing(20)
        self.proxyLayout.setContentsMargins(-1, -1, -1, 100)
        self.proxyCheckBox = QCheckBox(self.proxyPage)
        self.proxyCheckBox.setObjectName(u"proxyCheckBox")

        self.proxyLayout.addWidget(self.proxyCheckBox, 0, 0, 1, 1)

        self.proxyFrame = QFrame(self.proxyPage)
        self.proxyFrame.setObjectName(u"proxyFrame")
        self.proxyFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.proxyFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.proxyFrame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.proxyInputMethodCheckBox = QCheckBox(self.proxyFrame)
        self.proxyInputMethodCheckBox.setObjectName(u"proxyInputMethodCheckBox")
        self.proxyInputMethodCheckBox.setChecked(True)

        self.gridLayout_4.addWidget(self.proxyInputMethodCheckBox, 1, 0, 1, 1)

        self.btn_ok = QPushButton(self.proxyFrame)
        self.btn_ok.setObjectName(u"btn_ok")

        self.gridLayout_4.addWidget(self.btn_ok, 3, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter)

        self.proxyStatus = HighlightLabel(self.proxyFrame)
        self.proxyStatus.setObjectName(u"proxyStatus")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.proxyStatus.sizePolicy().hasHeightForWidth())
        self.proxyStatus.setSizePolicy(sizePolicy2)

        self.gridLayout_4.addWidget(self.proxyStatus, 0, 0, 1, 3)

        self.proxyInputDetailFrame = QFrame(self.proxyFrame)
        self.proxyInputDetailFrame.setObjectName(u"proxyInputDetailFrame")
        self.proxyInputDetailFrame.setMaximumSize(QSize(350, 16777215))
        self._3 = QGridLayout(self.proxyInputDetailFrame)
        self._3.setObjectName(u"_3")
        self._3.setContentsMargins(50, -1, -1, -1)
        self.proxyIpLabel = QLabel(self.proxyInputDetailFrame)
        self.proxyIpLabel.setObjectName(u"proxyIpLabel")

        self._3.addWidget(self.proxyIpLabel, 0, 0, 1, 1)

        self.proxyIpInput = QLineEdit(self.proxyInputDetailFrame)
        self.proxyIpInput.setObjectName(u"proxyIpInput")

        self._3.addWidget(self.proxyIpInput, 0, 1, 1, 1)

        self.proxyPortLabel = QLabel(self.proxyInputDetailFrame)
        self.proxyPortLabel.setObjectName(u"proxyPortLabel")

        self._3.addWidget(self.proxyPortLabel, 1, 0, 1, 1)

        self.proxyPortInput = QLineEdit(self.proxyInputDetailFrame)
        self.proxyPortInput.setObjectName(u"proxyPortInput")

        self._3.addWidget(self.proxyPortInput, 1, 1, 1, 1)

        self.proxyUserLabel = QLabel(self.proxyInputDetailFrame)
        self.proxyUserLabel.setObjectName(u"proxyUserLabel")

        self._3.addWidget(self.proxyUserLabel, 2, 0, 1, 1)

        self.proxyUserInput = QLineEdit(self.proxyInputDetailFrame)
        self.proxyUserInput.setObjectName(u"proxyUserInput")

        self._3.addWidget(self.proxyUserInput, 2, 1, 1, 1)

        self.proxyPassLabel = QLabel(self.proxyInputDetailFrame)
        self.proxyPassLabel.setObjectName(u"proxyPassLabel")

        self._3.addWidget(self.proxyPassLabel, 3, 0, 1, 1)

        self.proxyPassInput = QLineEdit(self.proxyInputDetailFrame)
        self.proxyPassInput.setObjectName(u"proxyPassInput")

        self._3.addWidget(self.proxyPassInput, 3, 1, 1, 1)


        self.gridLayout_4.addWidget(self.proxyInputDetailFrame, 2, 0, 1, 3)

        self.proxyInput = QLineEdit(self.proxyFrame)
        self.proxyInput.setObjectName(u"proxyInput")
        self.proxyInput.setMaximumSize(QSize(450, 16777215))

        self.gridLayout_4.addWidget(self.proxyInput, 1, 1, 1, 1)


        self.proxyLayout.addWidget(self.proxyFrame, 1, 0, 1, 1)

        self.pageStacked.addWidget(self.proxyPage)
        self.getPage = QWidget()
        self.getPage.setObjectName(u"getPage")
        self.gridLayout_7 = QGridLayout(self.getPage)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(15)
        self.gridLayout_7.setVerticalSpacing(0)
        self.getComboBox = QComboBox(self.getPage)
        self.getComboBox.addItem("")
        self.getComboBox.addItem("")
        self.getComboBox.setObjectName(u"getComboBox")
        sizePolicy.setHeightForWidth(self.getComboBox.sizePolicy().hasHeightForWidth())
        self.getComboBox.setSizePolicy(sizePolicy)
        self.getComboBox.setMinimumSize(QSize(210, 0))

        self.gridLayout_7.addWidget(self.getComboBox, 1, 0, 1, 1)

        self.statusGet = HighlightLabel(self.getPage)
        self.statusGet.setObjectName(u"statusGet")

        self.gridLayout_7.addWidget(self.statusGet, 4, 0, 1, 3)

        self.getStacked = QStackedWidget(self.getPage)
        self.getStacked.setObjectName(u"getStacked")
        self.loginPage = QWidget()
        self.loginPage.setObjectName(u"loginPage")
        self.gridLayout_5 = QGridLayout(self.loginPage)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(-1, -1, 25, -1)
        self.methodComboBox = QComboBox(self.loginPage)
        self.methodComboBox.addItem("")
        self.methodComboBox.addItem("")
        self.methodComboBox.setObjectName(u"methodComboBox")
        sizePolicy.setHeightForWidth(self.methodComboBox.sizePolicy().hasHeightForWidth())
        self.methodComboBox.setSizePolicy(sizePolicy)

        self.gridLayout_5.addWidget(self.methodComboBox, 0, 1, 1, 1)

        self.btn_reload_loginMethod = QPushButton(self.loginPage)
        self.btn_reload_loginMethod.setObjectName(u"btn_reload_loginMethod")
        self.btn_reload_loginMethod.setMaximumSize(QSize(43, 43))
        self.btn_reload_loginMethod.setIcon(icon6)
        self.btn_reload_loginMethod.setIconSize(QSize(30, 30))

        self.gridLayout_5.addWidget(self.btn_reload_loginMethod, 0, 2, 1, 1)

        self.methodLabel = QLabel(self.loginPage)
        self.methodLabel.setObjectName(u"methodLabel")
        sizePolicy1.setHeightForWidth(self.methodLabel.sizePolicy().hasHeightForWidth())
        self.methodLabel.setSizePolicy(sizePolicy1)

        self.gridLayout_5.addWidget(self.methodLabel, 0, 0, 1, 1)

        self.loginMethodStacked = QStackedWidget(self.loginPage)
        self.loginMethodStacked.setObjectName(u"loginMethodStacked")
        self.useUserPass = QWidget()
        self.useUserPass.setObjectName(u"useUserPass")
        self._5 = QGridLayout(self.useUserPass)
        self._5.setObjectName(u"_5")
        self._5.setContentsMargins(-1, -1, 0, -1)
        self.fullLoginInput = QLineEdit(self.useUserPass)
        self.fullLoginInput.setObjectName(u"fullLoginInput")

        self._5.addWidget(self.fullLoginInput, 1, 2, 1, 1)

        self.loginDetailFrame = QFrame(self.useUserPass)
        self.loginDetailFrame.setObjectName(u"loginDetailFrame")
        self.loginDetailFrame.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.loginDetailFrame.sizePolicy().hasHeightForWidth())
        self.loginDetailFrame.setSizePolicy(sizePolicy3)
        self._21 = QGridLayout(self.loginDetailFrame)
        self._21.setObjectName(u"_21")
        self._21.setContentsMargins(25, 0, 0, -1)
        self.userInput = QLineEdit(self.loginDetailFrame)
        self.userInput.setObjectName(u"userInput")

        self._21.addWidget(self.userInput, 0, 2, 1, 1)

        self.passLabel = QLabel(self.loginDetailFrame)
        self.passLabel.setObjectName(u"passLabel")

        self._21.addWidget(self.passLabel, 1, 0, 1, 1)

        self.passInput = QLineEdit(self.loginDetailFrame)
        self.passInput.setObjectName(u"passInput")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setBold(False)
        font.setItalic(False)
        self.passInput.setFont(font)

        self._21.addWidget(self.passInput, 1, 2, 1, 1)

        self.twoFAInput = QLineEdit(self.loginDetailFrame)
        self.twoFAInput.setObjectName(u"twoFAInput")

        self._21.addWidget(self.twoFAInput, 2, 2, 1, 1)

        self.twoFACheckBox = QCheckBox(self.loginDetailFrame)
        self.twoFACheckBox.setObjectName(u"twoFACheckBox")
        sizePolicy.setHeightForWidth(self.twoFACheckBox.sizePolicy().hasHeightForWidth())
        self.twoFACheckBox.setSizePolicy(sizePolicy)
        self.twoFACheckBox.setChecked(True)

        self._21.addWidget(self.twoFACheckBox, 2, 0, 1, 1)

        self.userLabel = QLabel(self.loginDetailFrame)
        self.userLabel.setObjectName(u"userLabel")
        self.userLabel.setFont(font)

        self._21.addWidget(self.userLabel, 0, 0, 1, 2)


        self._5.addWidget(self.loginDetailFrame, 2, 0, 1, 4)

        self.fullLoginCheckBox = QCheckBox(self.useUserPass)
        self.fullLoginCheckBox.setObjectName(u"fullLoginCheckBox")
        sizePolicy1.setHeightForWidth(self.fullLoginCheckBox.sizePolicy().hasHeightForWidth())
        self.fullLoginCheckBox.setSizePolicy(sizePolicy1)
        self.fullLoginCheckBox.setChecked(True)

        self._5.addWidget(self.fullLoginCheckBox, 1, 0, 1, 1)

        self.loginMethodStacked.addWidget(self.useUserPass)
        self.useCookie = QWidget()
        self.useCookie.setObjectName(u"useCookie")
        self._22 = QHBoxLayout(self.useCookie)
        self._22.setObjectName(u"_22")
        self.methodCookieLabel = QLabel(self.useCookie)
        self.methodCookieLabel.setObjectName(u"methodCookieLabel")

        self._22.addWidget(self.methodCookieLabel)

        self.cookieInput = HighlightPlainTextEdit(self.useCookie)
        self.cookieInput.setObjectName(u"cookieInput")

        self._22.addWidget(self.cookieInput)

        self.btn_copyCookie = QPushButton(self.useCookie)
        self.btn_copyCookie.setObjectName(u"btn_copyCookie")
        self.btn_copyCookie.setMaximumSize(QSize(50, 16777215))
        icon10 = QIcon()
        icon10.addFile(u":/icons/icons/copy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_copyCookie.setIcon(icon10)
        self.btn_copyCookie.setIconSize(QSize(40, 32))

        self._22.addWidget(self.btn_copyCookie)

        self.loginMethodStacked.addWidget(self.useCookie)

        self.gridLayout_5.addWidget(self.loginMethodStacked, 1, 0, 1, 6)

        self.btn_login = QPushButton(self.loginPage)
        self.btn_login.setObjectName(u"btn_login")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.btn_login.sizePolicy().hasHeightForWidth())
        self.btn_login.setSizePolicy(sizePolicy4)
        self.btn_login.setIconSize(QSize(40, 32))

        self.gridLayout_5.addWidget(self.btn_login, 2, 5, 1, 1)

        self.getStacked.addWidget(self.loginPage)
        self.getDataPage = QWidget()
        self.getDataPage.setObjectName(u"getDataPage")
        self.gridLayout_9 = QGridLayout(self.getDataPage)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.btn_getGroup = QPushButton(self.getDataPage)
        self.btn_getGroup.setObjectName(u"btn_getGroup")
        sizePolicy.setHeightForWidth(self.btn_getGroup.sizePolicy().hasHeightForWidth())
        self.btn_getGroup.setSizePolicy(sizePolicy)
        self.btn_getGroup.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.btn_getGroup, 2, 0, 1, 1)

        self.btn_getPost = QPushButton(self.getDataPage)
        self.btn_getPost.setObjectName(u"btn_getPost")
        sizePolicy.setHeightForWidth(self.btn_getPost.sizePolicy().hasHeightForWidth())
        self.btn_getPost.setSizePolicy(sizePolicy)
        self.btn_getPost.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.btn_getPost, 2, 1, 1, 1)

        self.getStacked.addWidget(self.getDataPage)

        self.gridLayout_7.addWidget(self.getStacked, 5, 0, 1, 3)

        self.btn_getReload = QPushButton(self.getPage)
        self.btn_getReload.setObjectName(u"btn_getReload")
        self.btn_getReload.setMaximumSize(QSize(43, 43))
        self.btn_getReload.setIcon(icon6)
        self.btn_getReload.setIconSize(QSize(30, 30))

        self.gridLayout_7.addWidget(self.btn_getReload, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_7.addItem(self.verticalSpacer, 6, 0, 1, 1)

        self.pageStacked.addWidget(self.getPage)

        self.vboxLayout.addWidget(self.pageStacked)

        self.bottomBar = QFrame(self.pageContainer)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setStyleSheet(u"background-color: rgb(44, 49, 58)")
        self._31 = QHBoxLayout(self.bottomBar)
        self._31.setSpacing(0)
        self._31.setObjectName(u"_31")
        self._31.setContentsMargins(0, 0, 0, 0)
        self.credits = QPushButton(self.bottomBar)
        self.credits.setObjectName(u"credits")
        icon11 = QIcon()
        icon11.addFile(u":/icons/icons/tele.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.credits.setIcon(icon11)

        self._31.addWidget(self.credits, 0, Qt.AlignmentFlag.AlignLeft)

        self.sizeGrip = QFrame(self.bottomBar)
        self.sizeGrip.setObjectName(u"sizeGrip")
        self.sizeGrip.setMinimumSize(QSize(22, 0))
        self.sizeGrip.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))

        self._31.addWidget(self.sizeGrip, 0, Qt.AlignmentFlag.AlignRight)


        self.vboxLayout.addWidget(self.bottomBar)


        self._14.addWidget(self.pageContainer, 1, 1, 1, 1)

        self.contentTop = QFrame(self.App)
        self.contentTop.setObjectName(u"contentTop")
        self.contentTop.setMinimumSize(QSize(0, 60))
        self._15 = QHBoxLayout(self.contentTop)
        self._15.setSpacing(0)
        self._15.setObjectName(u"_15")
        self._15.setContentsMargins(0, 0, 8, 0)
        self.icon = QLabel(self.contentTop)
        self.icon.setObjectName(u"icon")
        self.icon.setMinimumSize(QSize(60, 0))
        self.icon.setPixmap(QPixmap(u":/icons/icons/Logo.svg"))
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._15.addWidget(self.icon, 0, Qt.AlignmentFlag.AlignLeft)

        self.title = QLabel(self.contentTop)
        self.title.setObjectName(u"title")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy5)
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setBold(True)
        font1.setItalic(False)
        self.title.setFont(font1)

        self._15.addWidget(self.title)

        self.profileName = QPushButton(self.contentTop)
        self.profileName.setObjectName(u"profileName")
        self.profileName.setFont(font1)
        icon12 = QIcon()
        icon12.addFile(u":/icons/icons/account.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.profileName.setIcon(icon12)
        self.profileName.setIconSize(QSize(40, 40))

        self._15.addWidget(self.profileName)

        self.navigationBar = QFrame(self.contentTop)
        self.navigationBar.setObjectName(u"navigationBar")
        self._16 = QHBoxLayout(self.navigationBar)
        self._16.setSpacing(0)
        self._16.setObjectName(u"_16")
        self._16.setContentsMargins(0, 0, 0, 0)
        self.minimizeBtn = QPushButton(self.navigationBar)
        self.minimizeBtn.setObjectName(u"minimizeBtn")
        self.minimizeBtn.setFont(font1)
        icon13 = QIcon()
        icon13.addFile(u":/icons/icons/minimize.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeBtn.setIcon(icon13)
        self.minimizeBtn.setIconSize(QSize(20, 20))

        self._16.addWidget(self.minimizeBtn)

        self.changeWindowBtn = QPushButton(self.navigationBar)
        self.changeWindowBtn.setObjectName(u"changeWindowBtn")
        icon14 = QIcon()
        icon14.addFile(u":/icons/icons/maximize.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon14.addFile(u":/icons/icons/restore.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.changeWindowBtn.setIcon(icon14)
        self.changeWindowBtn.setIconSize(QSize(20, 20))
        self.changeWindowBtn.setCheckable(True)

        self._16.addWidget(self.changeWindowBtn)

        self.closeBtn = QPushButton(self.navigationBar)
        self.closeBtn.setObjectName(u"closeBtn")
        icon15 = QIcon()
        icon15.addFile(u":/icons/icons/close.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeBtn.setIcon(icon15)
        self.closeBtn.setIconSize(QSize(20, 20))

        self._16.addWidget(self.closeBtn)


        self._15.addWidget(self.navigationBar)


        self._14.addWidget(self.contentTop, 0, 0, 1, 2)

        self.pageContainer.raise_()
        self.leftMenu.raise_()
        self.contentTop.raise_()

        self.gridLayout_3.addWidget(self.App, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.pageStacked.setCurrentIndex(2)
        self.homeStackedWidget.setCurrentIndex(0)
        self.getStacked.setCurrentIndex(0)
        self.loginMethodStacked.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_toggle.setText(QCoreApplication.translate("MainWindow", u"   Hide", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"   Home", None))
        self.btn_get.setText(QCoreApplication.translate("MainWindow", u"   Get", None))
        self.btn_proxy.setText(QCoreApplication.translate("MainWindow", u"   Proxy", None))
        self.btn_save.setText(QCoreApplication.translate("MainWindow", u"   Save", None))
        self.statusHome.setText("")
        self.functionComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"POST", None))
        self.functionComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"COMMENT", None))
        self.functionComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"SPAM", None))

        self.postDelayLabel.setText(QCoreApplication.translate("MainWindow", u"\u0110\u1ed9 delay (s)", None))
        self.postDelayInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"gi\u1eefa 2 l\u1ea7n post", None))
        self.btn_post.setText("")
        self.postContentCheckBox.setText(QCoreApplication.translate("MainWindow", u"Content", None))
        self.postImageCheckBox.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.postContentInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nh\u1eadp content (C\u00f3 th\u1ebf nh\u1eadp theo list - ng\u0103n c\u00e1ch nhau b\u1edfi k\u00ed t\u1ef1 \"$\")", None))
        self.commentDelayLabel.setText(QCoreApplication.translate("MainWindow", u"\u0110\u1ed9 delay (s)", None))
        self.commentDelayInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"gi\u1eefa 2 l\u1ea7n comment", None))
        self.commentContentCheckBox.setText(QCoreApplication.translate("MainWindow", u"Content", None))
        self.commentImageCheckBox.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.commentContentInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nh\u1eadp content (C\u00f3 th\u1ebf nh\u1eadp theo list - ng\u0103n c\u00e1ch nhau b\u1edfi k\u00ed t\u1ef1 \"$\")", None))
        self.btn_comment.setText("")
        self.spamContentCheckBox.setText(QCoreApplication.translate("MainWindow", u"Content", None))
        self.spamImageCheckBox.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.spamContentInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nh\u1eadp content (C\u00f3 th\u1ebf nh\u1eadp theo list - ng\u0103n c\u00e1ch nhau b\u1edfi k\u00ed t\u1ef1 \"$\")", None))
        self.spamSpamDelayInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"th\u1eddi gian (s)", None))
        self.spamSpamDelay.setText(QCoreApplication.translate("MainWindow", u"\u0110\u1ed9 delay spam", None))
        self.spamPostNumber.setText(QCoreApplication.translate("MainWindow", u"S\u1ed1 post", None))
        self.spamScanDelayInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"th\u1eddi gian (s)", None))
        self.spamScrollNumber.setText(QCoreApplication.translate("MainWindow", u"S\u1ed1 l\u1ea7n cu\u1ed9n (qu\u00e9t post)", None))
        self.spamScanDelay.setText(QCoreApplication.translate("MainWindow", u"\u0110\u1ed9 delay qu\u00e9t post", None))
        self.btn_spam.setText(QCoreApplication.translate("MainWindow", u"SPAM!", None))
        self.spamListFilter.setPlaceholderText(QCoreApplication.translate("MainWindow", u"list t\u1eeb kh\u00f3a (ng\u0103n c\u00e1ch b\u1eddi k\u00ed t\u1ef1 \",\")", None))
        self.spamSpamListFilter.setText(QCoreApplication.translate("MainWindow", u"L\u1ecdc t\u1eeb kh\u00f3a", None))
        self.proxyCheckBox.setText(QCoreApplication.translate("MainWindow", u"PROXY", None))
        self.proxyInputMethodCheckBox.setText(QCoreApplication.translate("MainWindow", u"IP:PORT:USER:PASS", None))
        self.btn_ok.setText(QCoreApplication.translate("MainWindow", u"OK", None))
        self.proxyStatus.setText("")
        self.proxyIpLabel.setText(QCoreApplication.translate("MainWindow", u"IP", None))
        self.proxyIpInput.setText("")
        self.proxyPortLabel.setText(QCoreApplication.translate("MainWindow", u"PORT", None))
        self.proxyUserLabel.setText(QCoreApplication.translate("MainWindow", u"USER", None))
        self.proxyPassLabel.setText(QCoreApplication.translate("MainWindow", u"PASS", None))
        self.proxyPassInput.setText("")
        self.proxyInput.setText("")
        self.getComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"GET DATA", None))
        self.getComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"LOGIN", None))

        self.statusGet.setText("")
        self.methodComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Cookie", None))
        self.methodComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Username|Password|2fa", None))

        self.methodLabel.setText(QCoreApplication.translate("MainWindow", u"Login method", None))
        self.fullLoginInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"xxxxxxxxxx@gmail.com|**********|ABXDEFGH6572PJUS9I01JKK567GHJOPO", None))
        self.userInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"xxxxxxxxxx@gmail.com", None))
        self.passLabel.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.passInput.setText("")
        self.passInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"**********", None))
        self.twoFAInput.setText("")
        self.twoFAInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"ABXDEFGH6572PJUS9I01JKK567GHJOPO", None))
        self.twoFACheckBox.setText(QCoreApplication.translate("MainWindow", u"2FA", None))
        self.userLabel.setText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.fullLoginCheckBox.setText(QCoreApplication.translate("MainWindow", u"USER|PASS|2FA", None))
        self.methodCookieLabel.setText(QCoreApplication.translate("MainWindow", u"Cookie", None))
        self.cookieInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"c_user=...;fr=...;sb=...;xs=...;datr=...", None))
        self.btn_copyCookie.setText("")
        self.btn_login.setText(QCoreApplication.translate("MainWindow", u"LOGIN", None))
        self.btn_getGroup.setText(QCoreApplication.translate("MainWindow", u"GET GROUP", None))
        self.btn_getPost.setText(QCoreApplication.translate("MainWindow", u"GET POST", None))
        self.credits.setText(QCoreApplication.translate("MainWindow", u"contact: @Giang_vps", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"Tools Facebook", None))
        self.profileName.setText("")
    # retranslateUi

