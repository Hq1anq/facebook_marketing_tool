from selenium.webdriver.common.by import By
from PySide6.QtCore import QRunnable, Signal, Slot, QObject

from src.manager import DriverManager, DataManager

class GetGroup(QRunnable):
    class Signals(QObject):
        add_row = Signal(str, str)
        success = Signal(str)
        error = Signal(str)
        unlogin = Signal()
        finished = Signal()
        
    def __init__(self, driver_manager: DriverManager, data_manager: DataManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.data_manager = data_manager
        self.signals = self.Signals()

    @Slot()
    def run(self):
        if not self.driver_manager.setup_driver():
            self.signals.error.emit("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            self.signals.finished.emit()
            return
            
        self.driver_manager.jump_to_facebook()
        if not self.driver_manager.check_login():
            self.signals.unlogin.emit()
            self.signals.finished.emit()
            return

        self.driver = self.driver_manager.driver
        self.driver.set_window_size(800, 700)
        self.driver.set_window_position(0, 0)
        self.get_group()
            
    def get_group(self):
        self.driver.get("https://www.facebook.com/groups/joins")
        self.driver_manager.handle_chat_close()
        self.driver_manager.scroll_to_bottom()
        list_group = self.driver.find_elements(By.XPATH, f"//a[@aria-label='{self.driver_manager.view_group}']")
        if self.use_filter and self.filter_keys:
            for group in list_group:
                name = group.find_element(
                    By.XPATH,
                    "../../div[1]/div[2]//a"
                ).text.strip()
                if any(keyword in name.lower() for keyword in self.filter_keys):
                    link = group.get_attribute("href")
                    self.signals.add_row.emit(link, name)
        else:
            for group in list_group:
                link = group.get_attribute("href")
                name = group.find_element(
                    By.XPATH,
                    "../../div[1]/div[2]//a"
                ).text.strip()
                self.signals.add_row.emit(link, name)
        self.signals.success.emit("Đã lấy thông tin các group")
        self.signals.finished.emit()
    
    def setup(self, use_filter: bool, filter_keys: list):
        self.use_filter = use_filter
        self.filter_keys = filter_keys