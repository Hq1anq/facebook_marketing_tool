from PySide6.QtCore import Qt, QThreadPool

import src.settings as settings
from src.gui.custom_widget.image_viewer import ImageViewer
from src.manager import DataManager, DriverManager
from src.gui.widget.ui_interface import Ui_MainWindow
from src.gui.custom_widget.table_widget import TableWidget
from src.worker import Post
from src.utils import apply_int_range_validator

class PostUI:
    def __init__(self, before_run, handle_unlogin, table_widget: TableWidget, ui: Ui_MainWindow, data_manager: DataManager, driver_manager: DriverManager):
        self.before_run = before_run
        self.handle_unlogin = handle_unlogin
        self.table_widget = table_widget
        self.ui = ui
        self.data_manager = data_manager
        self.driver_manager = driver_manager
        self.image_viewer = ImageViewer(self.ui.postImageViewer, self.ui.postImageViewerWidget)

        self.worker = Post(self.driver_manager)
        self.worker.setAutoDelete(False)
        
        apply_int_range_validator(self.ui.postDelayInput)
        self.setup_connections()

    def setup_connections(self):
        self.ui.postImageCheckBox.stateChanged.connect(self.toggle_image_input)
        self.ui.postContentCheckBox.stateChanged.connect(self.toggle_content_input)
        self.ui.btn_postImageFromFile.clicked.connect(self.image_viewer.show_images)
        self.table_widget.btn_run.clicked.connect(self.run_post)

        self.worker.signals.log.connect(lambda msg: self.table_widget.statusTable.setText(msg))
        self.worker.signals.loading.connect(self.table_widget.statusTable.setLoading)
        self.worker.signals.table_status.connect(lambda row, status: self.table_widget.table.setItem(row, 4, self.table_widget.table_item(status, "center")))
        self.worker.signals.error.connect(self.table_widget.statusTable.setError)
        self.worker.signals.success.connect(self.table_widget.statusTable.setSuccess)
        self.worker.signals.unlogin.connect(self.on_unlogin_detected)
        self.worker.signals.finished.connect(lambda: self.table_widget.finish_action("POST", self.data_manager))

    def run_post(self):
        if self.table_widget.btn_run.text() != "POST": return
        self.before_run()
        if self.table_widget.btn_run.text() != "STOP POST!":
            self.save_data()
            post_data = self.data_manager.data["CONFIG"]["POST"]
            if not (post_data["image"] or post_data["content"]):
                self.ui.status.setError("POST: Thiếu thông tin để đăng bài")
                return
            
            self.table_widget.btn_run.setText("STOP POST!")
            self.worker.setup(
                self.table_widget.get_selected(),
                self.ui.postContentCheckBox.isChecked(),
                self.ui.postImageCheckBox.isChecked(),
                post_data["image"],
                post_data["content"],
                self.data_manager.data["CONFIG"]["POST"]["delay"] or self.data_manager.DEFAULT_DATA["POST"]["delay"]
            )
            self.worker.set_stop(False)  # Tell Spam to keep running
            QThreadPool.globalInstance().start(self.worker)
        else:
            self.table_widget.statusTable.setText("POST: Đã tạm dừng")
            self.table_widget.btn_run.setText("POST")
            self.worker.set_stop(True)
    
    def on_unlogin_detected(self):
        self.table_widget.hide()
        self.handle_unlogin()

    def load_data(self):
        content_string = "\n$\n".join(self.data_manager.data["CONFIG"]["POST"]["content"])
        self.ui.postContentInput.setPlainText(content_string)
        if len(self.data_manager.data["CONFIG"]["POST"]["delay"]) == 1:
            self.ui.postDelayInput.setText(str(self.data_manager.data["CONFIG"]["POST"]["delay"][0]))
        else:
            self.ui.postDelayInput.setText(
                f'{self.data_manager.data["CONFIG"]["POST"]["delay"][0]} - {self.data_manager.data["CONFIG"]["POST"]["delay"][1]}'
            )
        
    def load_image(self, use_dialog=False):
        self.image_viewer.show_images(self.data_manager.data["CONFIG"]["POST"]["image"], use_dialog=use_dialog)
    
    def save_data(self):
        self.data_manager.data["CONFIG"]["POST"]["image"] = self.image_viewer.list_image
        self.data_manager.data["CONFIG"]["POST"]["content"] = list(map(str.strip, self.ui.postContentInput.toPlainText().split("\n$\n")))
        delay = [int(x) for x in self.ui.postDelayInput.text().split('-') if x.strip().isdigit()]
        if not delay:
            delay = self.data_manager.DEFAULT_DATA["POST"]["delay"]
            self.ui.postDelayInput.setText(f'{delay[0]} - {delay[1]}')
        self.data_manager.data["CONFIG"]["POST"]["delay"] = delay
        
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