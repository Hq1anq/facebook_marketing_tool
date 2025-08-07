from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time, random, pyperclip
from PySide6.QtCore import QRunnable, Signal, Slot, QObject

from src.manager import DriverManager, DataManager

class Post(QRunnable):
    class Signals(QObject):
        log = Signal(str)
        table_status = Signal(int, str)
        finished = Signal()
        
    def __init__(self, driver_manager: DriverManager, data_manager: DataManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.data_manager = data_manager
        self.signals = self.Signals()
        self._stop = False

    @Slot()
    def run(self):
        self.post_delay = self.data_manager.data["POST"]["delay"] or self.data_manager.DEFAULT_DATA["POST"]["delay"]
        self.list_image = self.data_manager.data["POST"]["image"]
        self.list_content = self.data_manager.data["POST"]["content"]
        self.driver = self.driver_manager.driver
        if not self.table_data:
            self.signals.log.emit("Chọn ít nhất một group để đăng bài")
            self.signals.finished.emit()
            self.set_stop(True)
            return
        if not (self.use_content or self.use_image):
            self.signals.log.emit("Cần tối thiểu một content/image để đăng bài")
            self.signals.finished.emit()
            self.set_stop(True)
            return
        self.driver.set_window_size(800, 700)
        self.driver.set_window_position(0, 0)
        self.post()
    
    def post(self):
        countPost = 1
        for data in self.table_data:
            link_group = data["link"]
            name_group = data["name group"]
            if self._stop:
                self.signals.log.emit("POST: Đã tạm dừng")
                self.signals.finished.emit()
                return
            if all(keyword not in name_group for keyword in ["vps", "proxy", "rdp", "máy chủ", "server"]):
                self.signals.table_status.emit(data["row"], "Không phải nhóm VPS/Proxy")
                continue
            self.driver.get(link_group+"buy_sell_discussion")
            self.driver.execute_script("window.scrollTo(0, 300)")
            if "Bạn tạm thời bị chặn" in self.driver.page_source:
                self.signals.log.emit("POST : Bạn tạm thời bị chặn!")
                self.signals.finished.emit()
                self.set_stop(True)
                return
            try:
                self.signals.log.emit("POST: Đang đăng bài...")
                self.driver_manager.handle_chat_close()
                # Vào "Bạn viết gì đi..."
                create_post_btn = self.driver_manager.wait10.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".xkjl1po > .x1lliihq"))
                )
                self.driver_manager.click_element(create_post_btn)
                if self.use_content: # Paste content
                    content = random.choice(self.list_content)
                    pyperclip.copy(content)
                    content_area = self.driver_manager.wait10.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".\\_1mf"))
                    )
                    self.driver_manager.click_element(content_area)
                    # content_area.send_keys(Keys.CONTROL, "v")
                    self.driver_manager.actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

                # Thêm ảnh
                if self.use_image:
                    image = random.choice(self.list_image)
                    # add_image_btn = self.driver_manager.wait10.until(
                    #     EC.element_to_be_clickable((By.XPATH, f"//div[@aria-label='{self.driver_manager.add_image}']"))
                    # )
                    # self.driver_manager.click_element(add_image_btn)
                    self.driver.find_element(By.XPATH,"//input[@accept='image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv']").send_keys(image)
                time.sleep(1)
                self.driver.find_element(By.XPATH, f"//div[@aria-label='{self.driver_manager.post}']").click()
                time_delay = random.randint(self.post_delay[0], self.post_delay[len(self.post_delay)-1])
                if countPost % 10 == 0 and countPost < len(self.table_data): # Nghỉ mỗi 10 post
                    delay_each_10 = time_delay * random.randint(5, 10)
                    self.signals.log.emit("POST: Đã đăng " + str(countPost) + " bài, đợi " + str(delay_each_10) + "s rồi đăng tiếp")
                    time.sleep(delay_each_10)
                    self.signals.log.emit("POST: Đang đăng bài...")
                else:
                    time.sleep(time_delay) # Chờ post bài
                if "Để bảo vệ cộng đồng khỏi spam" in self.driver.page_source:
                    self.signals.table_status.emit(data["row"], "Bị chặn")
                    self.signals.log.emit("POST : Đã bị chặn, hãy nghỉ ngơi")
                    self.signals.finished.emit()
                    self.set_stop(True)
                    return
                self.signals.table_status.emit(data["row"], "Đã post")
            except:
                self.signals.table_status.emit(data["row"], "Chưa post")
                self.driver_manager.handle_chat_close()
            countPost += 1
        self.signals.log.emit("POST : Đã đăng xong!")
        self.signals.finished.emit()
        self.set_stop(True)
            
    def setup(self, table_data: list, use_content: bool, use_image: bool):
        self.table_data = table_data
        self.use_content = use_content
        self.use_image = use_image
            
    def set_stop(self, value: bool):
        self._stop = value