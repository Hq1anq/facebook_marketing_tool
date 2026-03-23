from PySide6.QtCore import Qt, QThreadPool

import src.settings as settings
from src.manager import DataManager, DriverManager
from src.gui.widget.ui_interface import Ui_MainWindow
from src.gui.custom_widget.table_widget import TableWidget
from src.worker import GetGroup, GetPost

class GetUI:
    def __init__(self, before_run, handle_unlogin, table_widget: TableWidget, ui: Ui_MainWindow, data_manager: DataManager, driver_manager: DriverManager):
        self.before_run = before_run
        self.handle_unlogin = handle_unlogin
        self.ui = ui
        self.data_manager = data_manager
        self.driver_manager = driver_manager
        self.table_widget = table_widget

        self.get_group = GetGroup(self.driver_manager, self.data_manager)
        self.get_group.setAutoDelete(False)
        self.get_post = GetPost(self.driver_manager, self.data_manager)
        self.get_post.setAutoDelete(False)

        self.setup_connections()
    
    def setup_connections(self):
        self.get_group.signals.add_row.connect(lambda link, name: self.table_widget.add_row(link, name))
        self.get_group.signals.success.connect(self.table_widget.statusTable.setSuccess)
        self.get_group.signals.finished.connect(self.table_widget.adjust_column_width)

        self.table_widget.btn_run.clicked.connect(self.on_table_btn_run_clicked)
        self.table_widget.tableExport.clicked.connect(self.on_table_export_clicked)

    def on_table_btn_run_clicked(self):
        if self.table_widget.btn_run.text() == "GET GROUP":
            self.run_getGroup()
        elif self.table_widget.btn_run.text() == "GET POST":
            self.run_getPost()

    def on_table_export_clicked(self):
        if self.table_widget.btn_run.text() == "GET GROUP" or "POST" in self.table_widget.btn_run.text():
            self.save_group_table()

    def run_getGroup(self):
        self.before_run()
        
        if not self.driver_manager.setup_driver():
            self.ui.status.setError("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            return
        self.driver_manager.jump_to_facebook()
        if not self.driver_manager.check_login():
            self.table_widget.hide()
            self.handle_unlogin()
            return
        
        filter_keys = [keyword.strip() for keyword in self.table_widget.filterGroupInput.text().split(",") if keyword.strip()]
        self.get_group.setup(self.table_widget.filterGroupCheckBox.isChecked(), filter_keys)
        
        self.table_widget.table.setRowCount(1) # Clear table
        self.table_widget.statusTable.setLoading("Đang lấy link group...")
        QThreadPool.globalInstance().start(self.get_group)

    def run_getPost(self):
        self.before_run()
        
        if not self.driver_manager.setup_driver():
            self.ui.status.setError("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            return
        self.driver_manager.jump_to_facebook()
        if not self.driver_manager.check_login():
            self.table_widget.hide()
            self.handle_unlogin()
            return

    def save_group_table(self):
        """Save current table content to data_manager.data['GET']['GROUP']"""
        group_list = []
        for row in range(1, self.table_widget.table.rowCount()): # except filter row
            link_group = self.table_widget.table.item(row, 0).text() if self.table_widget.table.item(row, 0) else ""
            link_post = self.table_widget.table.item(row, 1).text() if self.table_widget.table.item(row, 1) else ""
            name_group = self.table_widget.table.item(row, 2).text() if self.table_widget.table.item(row, 2) else ""
            status = self.table_widget.table.item(row, 3).text() if self.table_widget.table.item(row, 3) else ""

            group_data = {
                "link group": link_group,
                "link post": link_post,
                "name group": name_group,
                "status": status
            }
            group_list.append(group_data)

        # Save to data manager
        self.data_manager.data["GET"]["GROUP"] = group_list
        success = self.data_manager.save_data()
        
        if success:
            self.table_widget.statusTable.setText("Đã lưu dữ liệu bảng vào " + self.data_manager.data_path)
        else:
            self.table_widget.statusTable.setText("Lỗi: không thể lưu dữ liệu")