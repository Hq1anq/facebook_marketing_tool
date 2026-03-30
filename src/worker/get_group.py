from selenium.webdriver.common.by import By
from PySide6.QtCore import QRunnable, Signal, Slot, QObject

from src.manager import DriverManager

class GetGroup(QRunnable):
    class Signals(QObject):
        sync_groups = Signal(list)  # Emits full crawled list for merging
        loading = Signal(str)
        success = Signal(str)
        error = Signal(str)
        unlogin = Signal()
        finished = Signal()
        
    def __init__(self, driver_manager: DriverManager):
        super().__init__()
        self.driver_manager = driver_manager
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
        self.signals.loading.emit("Đang lấy danh sách group...")
        self.driver.get("https://www.facebook.com/groups/joins")
        self.driver_manager.handle_chat_close()
        self.driver_manager.scroll_to_bottom()
        
        list_group = self.driver.find_elements(By.XPATH, f"//a[@aria-label='{self.driver_manager.view_group}']")
        
        crawled_groups = []
        for group in list_group:
            try:
                name = group.find_element(
                    By.XPATH,
                    "../../div[1]/div[2]//a"
                ).text.strip()
                link = group.get_attribute("href")
                
                # Apply filter if enabled
                if self.use_filter and self.filter_keys:
                    if not any(keyword in name.lower() for keyword in self.filter_keys):
                        continue
                
                crawled_groups.append({"link group": link, "name group": name})
            except Exception:
                continue
        
        # Emit full list for merge instead of one-by-one
        self.signals.sync_groups.emit(crawled_groups)
        self.signals.success.emit(f"Đã lấy {len(crawled_groups)} group")
        self.signals.finished.emit()
    
    def setup(self, use_filter: bool, filter_keys: list):
        self.use_filter = use_filter
        self.filter_keys = filter_keys