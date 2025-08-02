# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tableWidgetsbibmw.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import resources.resources_rc

class Ui_tableWidget(object):
    def setupUi(self, tableWidget):
        if not tableWidget.objectName():
            tableWidget.setObjectName(u"tableWidget")
        tableWidget.resize(842, 553)
        tableWidget.setStyleSheet(u"*{ border: none }\n"
"#tableWidget { border: 9px solid rgb(40, 44, 52); border-radius: 18px }\n"
"#contentTop .QLabel { background-color: transparent; font-size: 15px }\n"
"QWidget {\n"
"	background-color: rgb(40, 44, 52);\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\" }\n"
"QPushButton {\n"
"	border: 3px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"	font-size: 15px; padding: 1px }\n"
"QPushButton:hover { background-color: rgb(57, 65, 80) }\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 3px solid rgb(43, 50, 61) }\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 3px;\n"
"	font-size: 15px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198) }\n"
"QLineEdit:hover { border: 2px solid rgb(64, 71, 88) }\n"
"QLineEdit:focus { border: 2px solid rgb(91, 101, 124) }\n"
"QCheckBox::indicator {\n"
""
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
"QTableWidget::item:selected{ background-color: rgb(189, 147, 249) }\n"
"QHeaderView { qproperty-defaultAlignment: AlignCenter }\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	font-size: 15px }\n"
"QScrollBar:horizontal {\n"
"	border: none;\n"
"	background: rgb(52, 59, 72);\n"
"	height: 8px;\n"
"	ma"
                        "rgin: 0px 21px 0 21px;\n"
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
"QScrollBar::sub-line:horizontal {\n"
"	border: none;\n"
"	background: rgb(55, 63, 77);\n"
"	width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"	border-bottom-left-radius: 4px;\n"
"	subcontrol-position: left;\n"
"	subcontrol-origin: margin }\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal,\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-pag"
                        "e:horizontal,\n"
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
"	subcontrol-position: bottom;\n"
"	subcontrol-origin: margin }\n"
"QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"	background: rgb(55, 63, 77);\n"
"	height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"	border-top-right-radius: 4px;\n"
"	subcontrol-position: top;\n"
"	subcontrol-origin: margin }\n"
"QScrollBar::add-line:horizontal:hover, QScrollBar::sub-line:horizontal:hover"
                        ",\n"
"QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {\n"
"	background: rgb(64, 69, 77) }\n"
"QScrollBar::add-line:horizontal:pressed, QScrollBar::sub-line:horizontal:pressed,\n"
"QScrollBar::add-line:vertical:pressed, QScrollBar::sub-line:vertical:pressed {\n"
"	background: rgb(189, 147, 249) }")
        self.verticalLayout = QVBoxLayout(tableWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.contentTop = QFrame(tableWidget)
        self.contentTop.setObjectName(u"contentTop")
        self.contentTop.setFrameShape(QFrame.Shape.StyledPanel)
        self.contentTop.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTop)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_run = QPushButton(self.contentTop)
        self.btn_run.setObjectName(u"btn_run")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_run.sizePolicy().hasHeightForWidth())
        self.btn_run.setSizePolicy(sizePolicy)
        self.btn_run.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.btn_run)

        self.btn_add = QPushButton(self.contentTop)
        self.btn_add.setObjectName(u"btn_add")
        sizePolicy.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy)
        self.btn_add.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.btn_add)

        self.btn_delete = QPushButton(self.contentTop)
        self.btn_delete.setObjectName(u"btn_delete")
        sizePolicy.setHeightForWidth(self.btn_delete.sizePolicy().hasHeightForWidth())
        self.btn_delete.setSizePolicy(sizePolicy)
        self.btn_delete.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.btn_delete)

        self.tableImport = QPushButton(self.contentTop)
        self.tableImport.setObjectName(u"tableImport")
        self.tableImport.setMaximumSize(QSize(100, 16777215))
        icon = QIcon()
        icon.addFile(u":/icons/icons/text2table.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tableImport.setIcon(icon)
        self.tableImport.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.tableImport)

        self.tableExport = QPushButton(self.contentTop)
        self.tableExport.setObjectName(u"tableExport")
        self.tableExport.setMaximumSize(QSize(100, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/table2text.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tableExport.setIcon(icon1)
        self.tableExport.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.tableExport)

        self.closeBtn = QPushButton(self.contentTop)
        self.closeBtn.setObjectName(u"closeBtn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.closeBtn.sizePolicy().hasHeightForWidth())
        self.closeBtn.setSizePolicy(sizePolicy1)
        self.closeBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(65, 74, 90);\n"
"	border: 4px solid rgb(65, 74, 90);\n"
"	border-radius: 10px; }\n"
"QPushButton:hover { background-color: rgb(52, 59, 72); border: 4px solid rgb(52, 59, 72) }\n"
"QPushButton:pressed { background-color: rgb(23, 26, 30); border: 4px solid rgb(23, 26, 30) }")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/close.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeBtn.setIcon(icon2)
        self.closeBtn.setIconSize(QSize(10, 12))

        self.horizontalLayout.addWidget(self.closeBtn, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)


        self.verticalLayout.addWidget(self.contentTop)

        self.latestPost = QFrame(tableWidget)
        self.latestPost.setObjectName(u"latestPost")
        self.horizontalLayout_2 = QHBoxLayout(self.latestPost)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(200, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.latestPostCheckBox = QCheckBox(self.latestPost)
        self.latestPostCheckBox.setObjectName(u"latestPostCheckBox")
        self.latestPostCheckBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.latestPostCheckBox)

        self.postIndex = QLineEdit(self.latestPost)
        self.postIndex.setObjectName(u"postIndex")
        self.postIndex.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.postIndex)

        self.horizontalSpacer_4 = QSpacerItem(200, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addWidget(self.latestPost, 0, Qt.AlignmentFlag.AlignTop)

        self.filterGroup = QFrame(tableWidget)
        self.filterGroup.setObjectName(u"filterGroup")
        self._2 = QHBoxLayout(self.filterGroup)
        self._2.setObjectName(u"_2")
        self._2.setContentsMargins(-1, 0, -1, 0)
        self.filterGroupCheckBox = QCheckBox(self.filterGroup)
        self.filterGroupCheckBox.setObjectName(u"filterGroupCheckBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.filterGroupCheckBox.sizePolicy().hasHeightForWidth())
        self.filterGroupCheckBox.setSizePolicy(sizePolicy2)
        self.filterGroupCheckBox.setChecked(True)

        self._2.addWidget(self.filterGroupCheckBox)

        self.filterGroupInput = QLineEdit(self.filterGroup)
        self.filterGroupInput.setObjectName(u"filterGroupInput")

        self._2.addWidget(self.filterGroupInput)


        self.verticalLayout.addWidget(self.filterGroup, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.fromToFrame = QFrame(tableWidget)
        self.fromToFrame.setObjectName(u"fromToFrame")
        self.horizontalLayout_5 = QHBoxLayout(self.fromToFrame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(150, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.listFrame = QFrame(self.fromToFrame)
        self.listFrame.setObjectName(u"listFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.listFrame.sizePolicy().hasHeightForWidth())
        self.listFrame.setSizePolicy(sizePolicy3)
        self.listFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.listFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.listFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.listLabel = QLabel(self.listFrame)
        self.listLabel.setObjectName(u"listLabel")

        self.horizontalLayout_4.addWidget(self.listLabel)


        self.horizontalLayout_5.addWidget(self.listFrame)

        self.listBox = QLineEdit(self.fromToFrame)
        self.listBox.setObjectName(u"listBox")

        self.horizontalLayout_5.addWidget(self.listBox)

        self.useFromToFrame = QFrame(self.fromToFrame)
        self.useFromToFrame.setObjectName(u"useFromToFrame")
        sizePolicy3.setHeightForWidth(self.useFromToFrame.sizePolicy().hasHeightForWidth())
        self.useFromToFrame.setSizePolicy(sizePolicy3)
        self.useFromToFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.useFromToFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.useFromToFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.fromLabel = QLabel(self.useFromToFrame)
        self.fromLabel.setObjectName(u"fromLabel")

        self.horizontalLayout_3.addWidget(self.fromLabel)

        self.fromBox = QLineEdit(self.useFromToFrame)
        self.fromBox.setObjectName(u"fromBox")
        self.fromBox.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.fromBox)

        self.toLabel = QLabel(self.useFromToFrame)
        self.toLabel.setObjectName(u"toLabel")

        self.horizontalLayout_3.addWidget(self.toLabel)

        self.toBox = QLineEdit(self.useFromToFrame)
        self.toBox.setObjectName(u"toBox")
        self.toBox.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.toBox)


        self.horizontalLayout_5.addWidget(self.useFromToFrame)

        self.btn_fromTo = QPushButton(self.fromToFrame)
        self.btn_fromTo.setObjectName(u"btn_fromTo")
        sizePolicy2.setHeightForWidth(self.btn_fromTo.sizePolicy().hasHeightForWidth())
        self.btn_fromTo.setSizePolicy(sizePolicy2)
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/change.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_fromTo.setIcon(icon3)

        self.horizontalLayout_5.addWidget(self.btn_fromTo)

        self.horizontalSpacer_2 = QSpacerItem(150, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.fromToFrame, 0, Qt.AlignmentFlag.AlignTop)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.statusTable = QLabel(tableWidget)
        self.statusTable.setObjectName(u"statusTable")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.statusTable.sizePolicy().hasHeightForWidth())
        self.statusTable.setSizePolicy(sizePolicy4)
        self.statusTable.setStyleSheet(u"color: yellow")
        self.statusTable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.statusTable)

        self.countRows = QLabel(tableWidget)
        self.countRows.setObjectName(u"countRows")

        self.horizontalLayout_6.addWidget(self.countRows)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.table = QTableWidget(tableWidget)
        if (self.table.columnCount() < 4):
            self.table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.table.setObjectName(u"table")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(sizePolicy5)
        self.table.setWordWrap(False)
        self.table.horizontalHeader().setMinimumSectionSize(110)
        self.table.horizontalHeader().setDefaultSectionSize(200)

        self.verticalLayout.addWidget(self.table)


        self.retranslateUi(tableWidget)

        QMetaObject.connectSlotsByName(tableWidget)
    # setupUi

    def retranslateUi(self, tableWidget):
        tableWidget.setWindowTitle(QCoreApplication.translate("tableWidget", u"Form", None))
        self.btn_run.setText(QCoreApplication.translate("tableWidget", u"OK", None))
        self.btn_add.setText(QCoreApplication.translate("tableWidget", u"ADD ROW", None))
        self.btn_delete.setText(QCoreApplication.translate("tableWidget", u"DELETE ROW", None))
        self.tableImport.setText(QCoreApplication.translate("tableWidget", u" IMPORT", None))
        self.tableExport.setText(QCoreApplication.translate("tableWidget", u" EXPORT", None))
        self.latestPostCheckBox.setText(QCoreApplication.translate("tableWidget", u"L\u1ea5y post m\u1edbi nh\u1ea5t", None))
        self.postIndex.setPlaceholderText(QCoreApplication.translate("tableWidget", u"\u0110i\u1ec1n s\u1ed1 th\u1ee9 t\u1ef1 post trong group", None))
        self.filterGroupCheckBox.setText(QCoreApplication.translate("tableWidget", u"Filter", None))
        self.filterGroupInput.setText("")
        self.filterGroupInput.setPlaceholderText(QCoreApplication.translate("tableWidget", u"vps, proxy, rdp", None))
        self.listLabel.setText(QCoreApplication.translate("tableWidget", u"List post", None))
        self.listBox.setPlaceholderText(QCoreApplication.translate("tableWidget", u"ng\u0103n c\u00e1ch nhau b\u1edbi d\u1ea5u ,", None))
        self.fromLabel.setText(QCoreApplication.translate("tableWidget", u"T\u1eeb post", None))
        self.fromBox.setText("")
        self.toLabel.setText(QCoreApplication.translate("tableWidget", u"\u0111\u1ebfn post", None))
        self.btn_fromTo.setText("")
        self.statusTable.setText("")
        self.countRows.setText(QCoreApplication.translate("tableWidget", u"Total rows:", None))
        ___qtablewidgetitem = self.table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("tableWidget", u"LINK GROUP", None));
        ___qtablewidgetitem1 = self.table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("tableWidget", u"LINK POST", None));
        ___qtablewidgetitem2 = self.table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("tableWidget", u"NAME GROUP", None));
        ___qtablewidgetitem3 = self.table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("tableWidget", u"STATUS", None));
    # retranslateUi

