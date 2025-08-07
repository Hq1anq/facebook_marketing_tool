from PySide6.QtCore import Qt

import src.settings as settings
from src.gui.custom_widget.image_viewer import ImageViewer
from src.gui.widget.ui_interface import Ui_MainWindow
from src.utils import apply_int_range_validator

from src.manager import DataManager

class CommentUI:
    def __init__(self, ui: Ui_MainWindow, data_manager: DataManager):
        self.ui = ui
        self.data_manager = data_manager
        self.image_viewer = ImageViewer(self.ui.commentImageViewer, self.ui.commentImageViewerWidget)
        
        apply_int_range_validator(self.ui.commentDelayInput)
        self.load_data()
        self.load_image()
        self.setup_connections()

    def setup_connections(self):
        self.ui.commentImageCheckBox.stateChanged.connect(self.toggle_image_input)
        self.ui.commentContentCheckBox.stateChanged.connect(self.toggle_content_input)
        self.ui.btn_commentImageFromFile.clicked.connect(self.image_viewer.show_images)
    
    def load_data(self):
        content_string = "\n$\n".join(self.data_manager.data["COMMENT"]["content"])
        self.ui.commentContentInput.setPlainText(content_string)
        self.ui.commentDelayInput.setText(
            str(self.data_manager.data["COMMENT"]["delay"]) if len(self.data_manager.data["COMMENT"]["delay"]) == 0
            else f'{self.data_manager.data["COMMENT"]["delay"][0]} - {self.data_manager.data["COMMENT"]["delay"][1]}'
        )
        
    def load_image(self, use_dialog=False):
        self.image_viewer.show_images(self.data_manager.data["COMMENT"]["image"], use_dialog=use_dialog)
    
    def save_data(self):
        self.data_manager.data["COMMENT"]["image"] = self.image_viewer.list_image
        self.data_manager.data["COMMENT"]["content"] = list(map(str.strip, self.ui.commentContentInput.toPlainText().split("\n$\n")))
        self.data_manager.data["COMMENT"]["delay"] = [int(x) for x in self.ui.commentDelayInput.text().split('-')]

    def toggle_image_input(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.commentImageViewer.show()
            self.ui.btn_commentImageFromFile.show()
            settings.commentImageInput = True
        else:
            self.ui.commentImageViewer.hide()
            self.ui.btn_commentImageFromFile.hide()
            settings.commentImageInput = False
            if settings.commentContentInput == False:
                settings.commentContentInput = True
                self.ui.commentContentCheckBox.blockSignals(True)
                self.ui.commentContentCheckBox.setCheckState(Qt.CheckState.Checked)
                self.ui.commentContentInput.show()
                self.ui.commentContentCheckBox.blockSignals(False)

    def toggle_content_input(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.commentContentInput.show()
            settings.commentContentInput = True
        else:
            self.ui.commentContentInput.hide()
            settings.commentContentInput = False
            if settings.commentImageInput == False:
                settings.commentImageInput = True
                self.ui.commentImageCheckBox.blockSignals(True)
                self.ui.commentImageCheckBox.setCheckState(Qt.CheckState.Checked)
                self.ui.btn_commentImageFromFile.show()
                self.ui.commentImageViewer.show()
                self.ui.commentImageCheckBox.blockSignals(False)