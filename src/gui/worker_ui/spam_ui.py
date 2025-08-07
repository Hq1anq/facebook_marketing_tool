from PySide6.QtCore import Qt

import src.settings as settings
from src.gui.custom_widget.image_viewer import ImageViewer
from src.manager import DataManager
from src.gui.widget.ui_interface import Ui_MainWindow
from src.utils import apply_int_range_validator

class SpamUI:
    def __init__(self, ui: Ui_MainWindow, data_manager: DataManager):
        self.ui = ui
        self.data_manager = data_manager
        self.image_viewer = ImageViewer(self.ui.spamImageViewer, self.ui.spamImageViewerWidget)
        
        apply_int_range_validator(self.ui.spamSpamDelayInput)
        apply_int_range_validator(self.ui.spamScanDelayInput)
        self.setup_connections()

    def setup_connections(self):
        self.ui.spamImageCheckBox.stateChanged.connect(self.toggle_image_input)
        self.ui.spamContentCheckBox.stateChanged.connect(self.toggle_content_input)
        self.ui.btn_spamImageFromFile.clicked.connect(self.image_viewer.show_images)
    
    def load_data(self):
        content_string = "\n$\n".join(self.data_manager.data["SPAM"]["content"])
        self.ui.spamContentInput.setPlainText(content_string)
        self.ui.spamScrollNumberInput.setText(str(self.data_manager.data["SPAM"]["scroll number"]))
        self.ui.spamPostNumberInput.setText(str(self.data_manager.data["SPAM"]["post number"]))
        self.ui.spamSpamDelayInput.setText(
            str(self.data_manager.data["SPAM"]["spam delay"]) if len(self.data_manager.data["SPAM"]["spam delay"]) == 0
            else f'{self.data_manager.data["SPAM"]["spam delay"][0]} - {self.data_manager.data["SPAM"]["spam delay"][1]}'
        )
        self.ui.spamScanDelayInput.setText(
            str(self.data_manager.data["SPAM"]["scan delay"]) if len(self.data_manager.data["SPAM"]["scan delay"]) == 0
            else f'{self.data_manager.data["SPAM"]["scan delay"][0]} - {self.data_manager.data["SPAM"]["scan delay"][1]}'
        )
        list_key_filter = ", ".join(self.data_manager.data["SPAM"]["key filter"])
        self.ui.spamListFilter.setText(list_key_filter)
        
    def load_image(self, use_dialog=False):
        self.image_viewer.show_images(self.data_manager.data["SPAM"]["image"], use_dialog=use_dialog)
    
    def save_data(self):
        spam_data = self.data_manager.data["SPAM"]
        default_data = self.data_manager.DEFAULT_DATA["SPAM"]
        spam_data["image"] = self.image_viewer.list_image
        spam_data["content"] = list(map(str.strip, self.ui.spamContentInput.toPlainText().split("\n$\n")))
        scroll_number = self.ui.spamScrollNumberInput.text().strip()
        if not scroll_number.isdigit():
            scroll_number = default_data["scroll number"]
            self.ui.spamScrollNumberInput.setText(str(spam_data["scroll number"]))
        spam_data["scroll number"] = int(scroll_number)
        
        post_number = self.ui.spamPostNumberInput.text().strip()
        if not post_number.isdigit():
            post_number = default_data["post number"]
            self.ui.spamPostNumberInput.setText(str(spam_data["post number"]))
        spam_data["post number"] = int(post_number)
        
        spam_delay = [int(x.strip()) for x in self.ui.spamSpamDelayInput.text().split('-') if x.strip().isdigit()]
        if not spam_delay:
            spam_delay = default_data["spam delay"]
            self.ui.spamSpamDelayInput.setText(f'{spam_delay[0]} - {spam_delay[1]}')
        spam_data["spam delay"] = spam_delay
        
        scan_delay = [int(x.strip()) for x in self.ui.spamScanDelayInput.text().split('-') if x.strip().isdigit()]
        if not scan_delay:
            scan_delay = default_data["scan delay"]
            self.ui.spamScanDelayInput.setText(f'{scan_delay[0]} - {scan_delay[1]}')
        spam_data["scan delay"] = scan_delay
        
        key_filter = list(map(str.strip, self.ui.spamListFilter.text().split(",")))
        if key_filter == [""]:
            key_filter = default_data["key filter"]
            self.ui.spamListFilter.setText(", ".join(key_filter))
        spam_data["key filter"] = key_filter

    def toggle_image_input(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.spamImageViewer.show()
            self.ui.btn_spamImageFromFile.show()
            settings.spamImageInput = True
        else:
            self.ui.spamImageViewer.hide()
            self.ui.btn_spamImageFromFile.hide()
            settings.spamImageInput = False
            if settings.spamContentInput == False:
                settings.spamContentInput = True
                self.ui.spamContentCheckBox.blockSignals(True)
                self.ui.spamContentCheckBox.setCheckState(Qt.CheckState.Checked)
                self.ui.spamContentInput.show()
                self.ui.spamContentCheckBox.blockSignals(False)

    def toggle_content_input(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.spamContentInput.show()
            settings.spamContentInput = True
        else:
            self.ui.spamContentInput.hide()
            settings.spamContentInput = False
            if settings.spamImageInput == False:
                settings.spamImageInput = True
                self.ui.spamImageCheckBox.blockSignals(True)
                self.ui.spamImageCheckBox.setCheckState(Qt.CheckState.Checked)
                self.ui.btn_spamImageFromFile.show()
                self.ui.spamImageViewer.show()
                self.ui.spamImageCheckBox.blockSignals(False)