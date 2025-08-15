from selenium.webdriver.common.by import By
from PySide6.QtCore import QRunnable, Signal, Slot, QObject

from src.manager import DriverManager, DataManager

class GetPost(QRunnable):
    class Signals(QObject):
        log = Signal(str)
        add_row = Signal(str, str)
        
    def __init__(self, driver_manager: DriverManager, data_manager: DataManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.data_manager = data_manager
        self.signals = self.Signals()

    @Slot()
    def run(self):
        self.driver = self.driver_manager.driver
        self.driver.set_window_size(800, 700)
        self.driver.set_window_position(0, 0)
        self.get_post()
            
    def get_post(self):
        self.driver.get("https://www.facebook.com/groups/joins")
        self.signals.log.emit("Đang lấy link group")
        self.driver_manager.handle_chat_close()
        self.driver_manager.scroll_to_bottom()
        list_group = self.driver.find_elements(By.XPATH, f"//a[@class='x1i10hfl xjbqb8w x1ejq31n x18oe1m7 x1sy0etr xstzfhl x972fbf x10w94by x1qhh985 x14e42zd x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x14z9mp xat24cr x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xkrqix3 x1sur9pj x1pd3egz']")
        i = 1
        if self.use_filter:
            for group in list_group:
                name = group.text
                if any(keyword in name for keyword in self.filter_keys):
                    link = group.get_attribute("href")
                    self.signals.add_row.emit(link, name)
        else:
            for group in list_group:
                link = group.get_attribute("href")
                name = group.text
                self.signals.add_row.emit(link, name)
        self.signals.log.emit("Đã lấy thông tin các group")
    
    def get_post_time(self):
        pass
    
    def setup(self, use_filter: bool, filter_keys: list):
        self.use_filter = use_filter
        self.filter_keys = filter_keys