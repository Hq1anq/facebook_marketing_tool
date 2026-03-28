from PySide6.QtCore import Qt, QThreadPool

import src.settings as settings
from src.gui.custom_widget.image_viewer import ImageViewer
from src.gui.widget.ui_interface import Ui_MainWindow
from src.utils import apply_int_range_validator
from src.worker import Comment

from src.manager import DataManager

class CommentUI:
    def __init__(self, before_run, handle_unlogin, table_widget, ui: Ui_MainWindow, data_manager: DataManager, driver_manager: DriverManager):
        self.before_run = before_run
        self.handle_unlogin = handle_unlogin
        self.table_widget = table_widget
        self.ui = ui
        self.data_manager = data_manager
        self.driver_manager = driver_manager
        self.image_viewer = ImageViewer(self.ui.commentImageViewer, self.ui.commentImageViewerWidget)
        
        self.worker = Comment(self.driver_manager)
        self.worker.setAutoDelete(False)
        
        apply_int_range_validator(self.ui.commentDelayInput)
        self.load_data()
        self.load_image()
        self.setup_connections()

    def setup_connections(self):
        self.ui.commentImageCheckBox.stateChanged.connect(self.toggle_image_input)
        self.ui.commentContentCheckBox.stateChanged.connect(self.toggle_content_input)
        self.ui.btn_commentImageFromFile.clicked.connect(self.image_viewer.show_images)
        
        self.worker.signals.log.connect(lambda msg: self.table_widget.statusTable.setText(msg))
        self.worker.signals.table_status.connect(lambda row, status: self.table_widget.table.setItem(row, 4, self.table_widget.table_item(status, "center")))
        self.worker.signals.error.connect(self.table_widget.statusTable.setError)
        self.worker.signals.finished.connect(self.on_finished)

    def run_comment(self):
        self.before_run()
        if self.table_widget.btn_run.text() != "STOP COMMENT!":
            self.save_data()
            comment_data = self.data_manager.data["CONFIG"]["COMMENT"]
            if not (comment_data["image"] or comment_data["content"]):
                self.ui.status.setError("COMMENT: Thiếu thông tin để comment")
                return
            if not self.driver_manager.check_login():
                self.handle_unlogin()
                return
            
            self.table_widget.btn_run.setText("STOP COMMENT!")
            self.worker.setup(
                self.table_widget.get_selected(),
                self.ui.commentContentCheckBox.isChecked(),
                self.ui.commentImageCheckBox.isChecked(),
                comment_data["image"],
                comment_data["content"],
                self.data_manager.data["CONFIG"]["COMMENT"]["delay"] or [3, 6]
            )
            self.worker.set_stop(False)
            QThreadPool.globalInstance().start(self.worker)
        else:
            self.table_widget.statusTable.setText("COMMENT: Đã tạm dừng")
            self.table_widget.btn_run.setText("COMMENT")
            self.worker.set_stop(True)

    def on_finished(self):
        self.table_widget.btn_run.setText("COMMENT")
        self.table_widget.adjust_column_width()
    
    def load_data(self):
        content_string = "\n$\n".join(self.data_manager.data["CONFIG"]["COMMENT"]["content"])
        self.ui.commentContentInput.setPlainText(content_string)
        self.ui.commentDelayInput.setText(
            str(self.data_manager.data["CONFIG"]["COMMENT"]["delay"]) if len(self.data_manager.data["CONFIG"]["COMMENT"]["delay"]) == 0
            else f'{self.data_manager.data["CONFIG"]["COMMENT"]["delay"][0]} - {self.data_manager.data["CONFIG"]["COMMENT"]["delay"][1]}'
        )
        
    def load_image(self, use_dialog=False):
        self.image_viewer.show_images(self.data_manager.data["CONFIG"]["COMMENT"]["image"], use_dialog=use_dialog)
    
    def save_data(self):
        self.data_manager.data["CONFIG"]["COMMENT"]["image"] = self.image_viewer.list_image
        self.data_manager.data["CONFIG"]["COMMENT"]["content"] = list(map(str.strip, self.ui.commentContentInput.toPlainText().split("\n$\n")))
        self.data_manager.data["CONFIG"]["COMMENT"]["delay"] = [int(x) for x in self.ui.commentDelayInput.text().split('-') if x.strip().isdigit()]

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