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
        self.get_group.signals.loading.connect(self.table_widget.statusTable.setLoading)
        self.get_group.signals.sync_groups.connect(
            lambda groups: self.table_widget.sync_groups_data(groups, self.data_manager)
        )
        self.get_group.signals.success.connect(self.table_widget.statusTable.setSuccess)
        self.get_group.signals.error.connect(self.table_widget.statusTable.setError)
        self.get_group.signals.unlogin.connect(self.on_unlogin_detected)
        self.get_group.signals.finished.connect(lambda: self.table_widget.finish_action("GET GROUP", self.data_manager))

        # Get Post
        self.get_post.signals.add_row.connect(
            lambda lg, ng, lp, c, s: self.table_widget.insert_post_for_group(link_group=lg, name_group=ng, link_post=lp, content=c, status=s)
        )
        self.get_post.signals.sync_posts.connect(
            lambda data: self.table_widget.sync_posts_data(data, self.data_manager)
        )
        self.get_post.signals.loading.connect(self.table_widget.statusTable.setLoading)
        self.get_post.signals.success.connect(self.table_widget.statusTable.setSuccess)
        self.get_post.signals.error.connect(self.table_widget.statusTable.setError)
        self.get_post.signals.unlogin.connect(self.on_unlogin_detected)
        self.get_post.signals.finished.connect(lambda: self.table_widget.finish_action("GET POST", self.data_manager))

        self.table_widget.btn_run.clicked.connect(self.open_table)

    def on_unlogin_detected(self):
        self.table_widget.hide()
        self.handle_unlogin()

    def open_table(self):
        if self.table_widget.btn_run.text() == "GET GROUP":
            self.run_getGroup()
        elif self.table_widget.btn_run.text() == "GET POST":
            self.run_getPost()

    def run_getGroup(self):
        self.before_run()
        self.table_widget.statusTable.setLoading("Đang lấy link group...")
        
        filter_keys = [keyword.strip() for keyword in self.table_widget.filterGroupInput.text().split(",") if keyword.strip()]
        self.get_group.setup(self.table_widget.filterGroupCheckBox.isChecked(), filter_keys)
        
        QThreadPool.globalInstance().start(self.get_group)

    def run_getPost(self):
        self.before_run()
        self.table_widget.statusTable.setLoading("Đang lấy link post từ các group...")

        selected_groups = self.table_widget.get_selected()
        if not selected_groups:
            self.table_widget.statusTable.setError("Vui lòng chọn ít nhất một group trong bảng")
            return

        self.get_post.setup(selected_groups)

        QThreadPool.globalInstance().start(self.get_post)
