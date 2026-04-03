# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tableWidgetQNxwVh.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout)

from src.gui.custom_widget.highlighted_widget import HighlightLabel
import resources.resources_rc

class Ui_tableWidget(object):
    def setupUi(self, tableWidget):
        if not tableWidget.objectName():
            tableWidget.setObjectName(u"tableWidget")
        tableWidget.resize(842, 553)
        tableWidget.setStyleSheet(u"background-color: transparent")
        self.verticalLayout = QVBoxLayout(tableWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(15, 0, 15, 15)
        self.contentFrame = QFrame(tableWidget)
        self.contentFrame.setObjectName(u"contentFrame")
        self.contentFrame.setStyleSheet(u"*{ border: none }\n"
"#contentFrame { border: 9px solid rgb(40, 44, 52); border-radius: 18px }\n"
"#contentTop .QLabel { background-color: transparent; font-size: 15px }\n"
"QWidget {\n"
"	background-color: rgb(40, 44, 52);\n"
"	color: rgb(221, 221, 221);\n"
"	font: 12pt \"Segoe UI\" }\n"
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
"	selection-background-color: rgb(255, 121, 198);\n"
"    selection-color: rgb(40, 44, 52) }\n"
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
"	border-top-right"
                        "-radius: 4px;\n"
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
"	background: rgb(55, "
                        "63, 77);\n"
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
"QScrollBar::add-line:horizontal:hover, QScrollBar::sub-line:horizontal:hover,\n"
"QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {\n"
"	background: rgb(64, 69, 77) }\n"
"QScrollBar::add-line:horizontal:pressed, QScrollBar::sub-line:horizontal:pressed,\n"
"QScrollBar::add-line:vertical:pressed, QScrollBar::sub-line:vertical:pressed {\n"
"	background: rgb(189, 147, 249) }\n"
"#countRows, #statusTable { font-size: 14pt }")
        self.contentFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.contentFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.contentTop = QFrame(self.contentFrame)
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


        self.verticalLayout_2.addWidget(self.contentTop)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.statusTable = HighlightLabel(self.contentFrame)
        self.statusTable.setObjectName(u"statusTable")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.statusTable.sizePolicy().hasHeightForWidth())
        self.statusTable.setSizePolicy(sizePolicy2)
        self.statusTable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.statusTable)

        self.countRows = QLabel(self.contentFrame)
        self.countRows.setObjectName(u"countRows")

        self.horizontalLayout_6.addWidget(self.countRows)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.table = QTableWidget(self.contentFrame)
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
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(sizePolicy3)
        self.table.setStyleSheet(u"QTableCornerButton::section { background-color: rgb(33, 37, 43) }\n"
"QTableWidget {	\n"
"	padding: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60); }\n"
"QTableWidget::item{ border-color: rgb(44, 49, 60) }\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(40, 44, 52);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	font-size: 15px }\n"
"QLineEdit {\n"
"    background-color: rgb(50, 54, 62); /* slightly lighter/darker variant for edit mode */\n"
"	selection-background-color: rgb(189, 147, 249); /* background when highlight */\n"
"    selection-color: rgb(40, 44, 52); /* text color when selected */\n"
"}")
        self.table.setWordWrap(False)
        self.table.horizontalHeader().setMinimumSectionSize(110)
        self.table.horizontalHeader().setDefaultSectionSize(200)

        self.verticalLayout_2.addWidget(self.table)


        self.verticalLayout.addWidget(self.contentFrame)


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

