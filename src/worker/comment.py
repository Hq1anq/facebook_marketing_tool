from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, random, pyperclip
from PySide6.QtCore import QRunnable, Signal, Slot, QObject

from src.manager import DriverManager

class Comment(QRunnable):
    class Signals(QObject):
        log = Signal(str)
        table_status = Signal(int, str)
        error = Signal(str)
        finished = Signal()
        
    def __init__(self, driver_manager: DriverManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.signals = self.Signals()
        self._stop = False
    
    def setup(self, table_data: list, use_content: bool, use_image: bool, list_image, list_content, comment_delay):
        self.table_data = table_data
        self.use_content = use_content
        self.use_image = use_image
        self.list_image = list_image
        self.list_content = list_content
        self.comment_delay = comment_delay

    @Slot()
    def run(self):
        self.driver = self.driver_manager.driver
        if not self.table_data:
            self.signals.log.emit("COMMENT: Chọn ít nhất một post để comment")
            self.signals.finished.emit()
            self.set_stop(True)
            return
        if not (self.use_content or self.use_image):
            self.signals.log.emit("COMMENT: Cần tối thiểu một content/image để comment")
            self.signals.finished.emit()
            self.set_stop(True)
            return
            
        if not self.driver_manager.setup_driver():
            self.signals.error.emit("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            self.signals.finished.emit()
            return

        self.driver.set_window_size(800, 700)
        self.driver.set_window_position(0, 0)
        self.comment()
    
    def comment(self):
        countComment = 1
        for data in self.table_data:
            link_post = data["link post"]
            if self._stop:
                self.signals.log.emit("COMMENT: Đã tạm dừng")
                self.signals.finished.emit()
                return
            
            if not link_post:
                self.signals.table_status.emit(data["row"], "Thiếu link post")
                continue

            self.driver.get(link_post)
            time.sleep(2)
            
            if "Bạn tạm thời bị chặn" in self.driver.page_source:
                self.signals.log.emit("COMMENT: Bạn tạm thời bị chặn!")
                self.signals.finished.emit()
                self.set_stop(True)
                return
                
            try:
                self.signals.log.emit(f"COMMENT: Đang comment vào post {countComment}...")
                self.driver_manager.handle_chat_close()
                
                # Find comment box
                comment_box = self.driver_manager.wait_for_clickable_element(By.CSS_SELECTOR, "div[aria-label='Viết bình luận'], div[aria-label='Write a comment']")
                self.driver_manager.click_element(comment_box)
                
                if self.use_content:
                    content = random.choice(self.list_content)
                    pyperclip.copy(content)
                    self.driver_manager.actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                
                if self.use_image:
                    image = random.choice(self.list_image)
                    self.driver.find_element(By.XPATH, "//input[@accept='image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv']").send_keys(image)
                    time.sleep(1)

                self.driver_manager.actions.send_keys(Keys.ENTER).perform()
                
                time_delay = random.randint(self.comment_delay[0], self.comment_delay[-1] if len(self.comment_delay) > 1 else self.comment_delay[0])
                time.sleep(time_delay)
                
                self.signals.table_status.emit(data["row"], "Đã comment")
            except Exception as e:
                self.signals.table_status.emit(data["row"], "Chưa comment")
                self.driver_manager.handle_chat_close()
                
            countComment += 1
            
        self.signals.log.emit("COMMENT: Đã comment xong!")
        self.signals.finished.emit()
        self.set_stop(True)
            
    def set_stop(self, value: bool):
        self._stop = value