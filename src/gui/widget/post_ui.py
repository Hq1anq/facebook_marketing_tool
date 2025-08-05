from PySide6.QtCore import Qt

import src.settings as settings
from src.gui.custom_widget.image_viewer import ImageViewer
from src.manager import DataManager
from src.gui.widget.ui_interface import Ui_MainWindow

class PostUI:
    def __init__(self, ui: Ui_MainWindow, data_manager: DataManager):
        self.ui = ui
        self.data_manager = data_manager
        self.image_viewer = ImageViewer(self.ui.postImageViewer, self.ui.postImageViewerWidget)
        
        self.setup_connections()

    def setup_connections(self):
        self.ui.postImageCheckBox.stateChanged.connect(self.toggle_image_input)
        self.ui.postContentCheckBox.stateChanged.connect(self.toggle_content_input)
        self.ui.btn_postImageFromFile.clicked.connect(self.image_viewer.show_images)

    def load_data(self):
        content_string = "\n$\n".join(self.data_manager.data["POST"]["content"])
        self.ui.postContentInput.setPlainText(content_string)
        self.ui.postDelayInput.setText(
            str(self.data_manager.data["POST"]["delay"]) if len(self.data_manager.data["POST"]["delay"]) == 0
            else f'{self.data_manager.data["POST"]["delay"][0]} - {self.data_manager.data["POST"]["delay"][1]}'
        )
        
    def load_image(self, use_dialog=False):
        self.image_viewer.show_images(self.data_manager.data["POST"]["image"], use_dialog=use_dialog)
    
    def save_data(self):
        self.data_manager.data["POST"]["image"] = self.image_viewer.list_image
        self.data_manager.data["POST"]["content"] = list(map(str.strip, self.ui.postContentInput.toPlainText().split("\n$\n")))
        self.data_manager.data["POST"]["delay"] = [int(x) for x in self.ui.postDelayInput.text().split('-')]
        
    def toggle_image_input(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.postImageViewer.show()
            self.ui.btn_postImageFromFile.show()
            settings.postImageInput = True
        else:
            self.ui.postImageViewer.hide()
            self.ui.btn_postImageFromFile.hide()
            settings.postImageInput = False
            if settings.postContentInput == False:
                settings.postContentInput = True
                self.ui.postContentCheckBox.blockSignals(True)
                self.ui.postContentCheckBox.setCheckState(Qt.CheckState.Checked)
                self.ui.postContentInput.show()
                self.ui.postContentCheckBox.blockSignals(False)

    def toggle_content_input(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.postContentInput.show()
            settings.postContentInput = True
        else:
            self.ui.postContentInput.hide()
            settings.postContentInput = False
            if settings.postImageInput == False:
                settings.postImageInput = True
                self.ui.postImageCheckBox.blockSignals(True)
                self.ui.postImageCheckBox.setCheckState(Qt.CheckState.Checked)
                self.ui.btn_postImageFromFile.show()
                self.ui.postImageViewer.show()
                self.ui.postImageCheckBox.blockSignals(False)