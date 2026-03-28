from PySide6.QtCore import QThreadPool

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

        self.get_group = GetGroup(self.driver_manager)
        self.get_group.setAutoDelete(False)
        self.get_post = GetPost(self.driver_manager)
        self.get_post.setAutoDelete(False)

        self.setup_connections()
    
    def setup_connections(self):
        # Get Group
        self.get_group.signals.add_row.connect(
            lambda lg, ng, lp, c, s: self.table_widget.add_row(link_group=lg, name_group=ng, link_post=lp, content=c, status=s)
        )
        self.get_group.signals.success.connect(self.table_widget.statusTable.setSuccess)
        self.get_group.signals.error.connect(self.ui.status.setError)
        self.get_group.signals.unlogin.connect(self.on_unlogin_detected)
        self.get_group.signals.finished.connect(self.table_widget.adjust_column_width)

        # Get Post
        self.get_post.signals.add_row.connect(
            lambda lg, ng, lp, c, s: self.table_widget.add_row(link_group=lg, name_group=ng, link_post=lp, content=c, status=s)
        )
        self.get_post.signals.success.connect(self.table_widget.statusTable.setSuccess)
        self.get_post.signals.error.connect(self.ui.status.setError)
        self.get_post.signals.unlogin.connect(self.on_unlogin_detected)
        self.get_post.signals.finished.connect(self.table_widget.adjust_column_width)

        self.table_widget.btn_run.clicked.connect(self.on_table_btn_run_clicked)
        self.table_widget.tableExport.clicked.connect(self.on_table_export_clicked)

    def on_unlogin_detected(self):
        self.table_widget.hide()
        self.handle_unlogin()

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
        self.table_widget.statusTable.setLoading("Đang lấy link group...")
        
        filter_keys = [keyword.strip() for keyword in self.table_widget.filterGroupInput.text().split(",") if keyword.strip()]
        self.get_group.setup(self.table_widget.filterGroupCheckBox.isChecked(), filter_keys)
        
        self.table_widget.table.setRowCount(1) # Clear table
        QThreadPool.globalInstance().start(self.get_group)

    def run_getPost(self):
        self.before_run()

        selected_groups = self.table_widget.get_selected()
        if not selected_groups:
            self.ui.status.setError("Vui lòng chọn ít nhất một group trong bảng")
            return

        self.table_widget.statusTable.setLoading("Đang lấy link post...")

        filter_keys = [keyword.strip() for keyword in self.table_widget.filterGroupInput.text().split(",") if keyword.strip()]
        self.get_post.setup(self.table_widget.filterGroupCheckBox.isChecked(), filter_keys, selected_groups)

        self.table_widget.table.setRowCount(1) # Clear table
        QThreadPool.globalInstance().start(self.get_post)

    def save_group_table(self):
        """Save current table content to data_manager.data['TABLE'] using nested structure"""
        original_table = self.data_manager.data.get("TABLE", [])
        new_table_data = [] # List of groups
        
        def find_group_in_new(link):
            for g in new_table_data:
                if g["link group"] == link: return g
            return None

        def find_group_in_orig(link):
            for g in original_table:
                if g["link group"] == link: return g
            return None

        def find_post_in_group(group, lp, c):
            if not group: return None
            for p in group.get("posts", []):
                if lp and p.get("link post") == lp: return p
                if not lp and c and p.get("content") == c: return p
            return None

        for row in range(1, self.table_widget.table.rowCount()): # skip filter row
            lg = self.table_widget.table.item(row, 0).text() if self.table_widget.table.item(row, 0) else ""
            ng = self.table_widget.table.item(row, 1).text() if self.table_widget.table.item(row, 1) else ""
            lp = self.table_widget.table.item(row, 2).text() if self.table_widget.table.item(row, 2) else ""
            c = self.table_widget.table.item(row, 3).text() if self.table_widget.table.item(row, 3) else ""
            st = self.table_widget.table.item(row, 4).text() if self.table_widget.table.item(row, 4) else ""

            group = find_group_in_new(lg)
            if not group:
                group = {"link group": lg, "name group": ng, "posts": []}
                new_table_data.append(group)
            
            # Find original data to preserve non-active statuses
            orig_group = find_group_in_orig(lg)
            orig_post = find_post_in_group(orig_group, lp, c)
            
            post_data = {
                "link post": lp,
                "content": c,
                "status_post": orig_post.get("status_post", "") if orig_post else "",
                "status_comment": orig_post.get("status_comment", "") if orig_post else ""
            }
            
            # Update only the current mode's status
            if self.table_widget.current_mode == "COMMENT":
                post_data["status_comment"] = st
            else:
                post_data["status_post"] = st
            
            if lp or c or st:
                group["posts"].append(post_data)

        # Update and save
        self.data_manager.data["TABLE"] = new_table_data
        success = self.data_manager.save_data()
        
        if success:
            self.table_widget.statusTable.setText("Đã lưu dữ liệu bảng vào " + self.data_manager.data_path)
        else:
            self.table_widget.statusTable.setText("Lỗi: không thể lưu dữ liệu")