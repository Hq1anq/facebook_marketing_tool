from selenium.webdriver.common.by import By
from PySide6.QtCore import QRunnable, Signal, Slot, QObject

from src.manager import DriverManager

class GetPost(QRunnable):
    class Signals(QObject):
        log = Signal(str)
        add_row = Signal(str, str, str, str, str)
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
        self.get_post()
            
    def get_post(self):
        self.signals.log.emit("Đang lấy link post từ các group...")
        self.driver_manager.handle_chat_close()
        
        for group in self.group_list:
            link_group = group.get("link group", "")
            name_group = group.get("name group", "")
            
            if not link_group:
                continue
                
            self.signals.log.emit(f"Đang vào group: {name_group}")
            self.driver.get(link_group)
            self.driver_manager.scroll(1) # Scroll little to load more
            
            # Extract post links
            post_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/posts/') or contains(@href, '/permalink/')]")
            
            post_links = set()
            for elem in post_elements:
                link = elem.get_attribute("href")
                if link and "/groups/" in link:
                    clean_link = link.split("?")[0].rstrip("/")
                    post_links.add(clean_link)
            
            for link in post_links:
                self.signals.add_row.emit(link_group, name_group, link, "", "")
                    
        self.signals.success.emit("Đã lấy thông tin các post")
        self.signals.finished.emit()
    
    def get_post_time(self):
        pass
    
    def setup(self, use_filter: bool, filter_keys: list, group_list: list = None):
        self.use_filter = use_filter
        self.filter_keys = filter_keys