from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time, random, pickle, pyperclip, os
from PySide6.QtCore import Qt, QRunnable, Signal, Slot, QObject

from src.manager import DriverManager, DataManager

class Spam(QRunnable):
    class Signals(QObject):
        log = Signal(str)
        finished = Signal(str)
        
    def __init__(self, driver_manager: DriverManager, data_manager: DataManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.data_manager = data_manager
        self.signals = self.Signals()
        self._stop = False

    @Slot()
    def run(self):
        self.scroll_number = self.data_manager.data["SPAM"]["scroll number"] or self.data_manager.DEFAULT_DATA["SPAM"]["scroll number"]
        self.post_number = self.data_manager.data["SPAM"]["post number"] or self.data_manager.DEFAULT_DATA["SPAM"]["post number"]
        self.spam_delay = self.data_manager.data["SPAM"]["spam delay"] or self.data_manager.DEFAULT_DATA["SPAM"]["spam delay"]
        self.scan_delay = self.data_manager.data["SPAM"]["scan delay"] or self.data_manager.DEFAULT_DATA["SPAM"]["scan delay"]
        self.key_filter = self.data_manager.data["SPAM"]["key filter"] or self.data_manager.DEFAULT_DATA["SPAM"]["key filter"]
        self.list_image = self.data_manager.data["SPAM"]["image"]
        self.list_content = self.data_manager.data["SPAM"]["content"]
        self.driver = self.driver_manager.driver
        self.spam()
            
    def spam(self, spam_limit = 100):
        commented_path = os.path.join(self.data_manager.folder_path, "commented.pkl")
        if os.path.exists(commented_path):
            with open(commented_path, "rb") as file:
                commented_id = pickle.load(file)
        else: commented_id = set()
        countSpam = 0
        countReload = 0
        while not self._stop:
            self.signals.log.emit("SPAM: Đang spam các post trong news feed")
            self.driver.get("https://www.facebook.com/?filter=groups&sk=h_chr")
            countReload += 1
            for _ in range(int(self.scroll_number)):
                self.driver_manager.scroll(3)
                feed_links = self.driver.find_elements(By.XPATH,"//div[@class='x6prxxf xk50ysn xvq8zen']/span[1]/span[1]/a[1]")
                for feed_link in feed_links:
                    postID = feed_link.get_attribute("href").split("permalinks=")[1].split("&__")[0]
                    if (postID in commented_id): # Check xem post đã được comment hay chưa
                        break
                    group_name = feed_link.text.lower()
                    if ("vps" not in group_name) and ("proxy" not in group_name): # Check điều kiện group
                        break
                    try:
                        self.driver.set_window_size(800, 700)
                        self.driver.set_window_position(0, 0)
                        self.driver_manager.handle_chat_close()
                        feed_div = feed_link.find_element(By.XPATH, "../../../../../../../../../../../..")
                        post_content = feed_div.find_element(By.XPATH,"div[3]/div[1]/div[1]/div[1]").text.lower()
                        comment_condition = False # chỉ False nếu có filter checkbox được check và các item trong listkey đều không có trong content
                        if self.ui.spamSpamListFilter.checkState() == Qt.CheckState.Checked:
                            for key in self.key_filter:
                                if key in post_content:
                                    comment_condition = True
                                    break
                        else: comment_condition = True
                        if comment_condition:
                            comment_div = feed_div.find_element(By.XPATH, "div[4]/div[1]/div[1]")
                            comment_btn = self.driver_manager.wait10.until(
                                EC.element_to_be_clickable((By.XPATH, f"//div[@aria-label='{self.driver_manager.comment_aria}']"))
                            )
                            self.driver_manager.click_element(comment_btn)
                            if self.check_open_post():
                                text_box = self.driver.find_element(By.XPATH, "//div[@class='xwib8y2 xurb0ha x1y1aw1k']//div[@role='textbox']")
                                if self.list_image:
                                    image = random.choice(self.list_image)
                                    img_div = text_box.find_element(By.XPATH, "../../../../../..//input[@accept='video/*,  video/x-m4v, video/webm, video/x-ms-wmv, video/x-msvideo, video/3gpp, video/flv, video/x-flv, video/mp4, video/quicktime, video/mpeg, video/ogv, .ts, .mkv, image/*, image/heic, image/heif']")
                                    img_div.send_keys(image)
                                self.driver_manager.click_element(text_box)
                                if self.list_content:
                                    content = random.choice(self.list_content)
                                    pyperclip.copy(content)
                                    self.driver_manager.actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                                self.driver_manager.actions.send_keys(Keys.ENTER).perform()
                                time.sleep(random.randint(self.spam_delay[0], self.spam_delay[len(self.spam_delay) - 1]))
                                close = self.driver.find_element(By.XPATH, "//div[@aria-label='Đóng']")
                                self.driver_manager.click_element(close)
                            else:
                                text_box = comment_div.find_element(By.XPATH, ".//div[@role='textbox']")
                                if self.list_image:
                                    image = random.choice(self.list_image)
                                    pic_div = comment_div.find_element(By.XPATH, ".//input[@accept='video/*,  video/x-m4v, video/webm, video/x-ms-wmv, video/x-msvideo, video/3gpp, video/flv, video/x-flv, video/mp4, video/quicktime, video/mpeg, video/ogv, .ts, .mkv, image/*, image/heic, image/heif']")
                                    pic_div.send_keys(image)
                                self.driver_manager.click_element(text_box)
                                if self.list_content:
                                    content = random.choice(self.list_content)
                                    pyperclip.copy(content)
                                    self.driver_manager.actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                                self.driver_manager.actions.send_keys(Keys.ENTER).perform()
                                time.sleep(random.randint(self.spam_delay[0], self.spam_delay[len(self.spam_delay)-1]))
                            if "Không thể đăng bình luận" in self.driver.page_source:
                                self.signals.finished.emit()
                                self.signals.log.emit("SPAM: Đã bị chặn comment, hãy nghỉ ngơi")
                                self._stop = True
                                
                                with open(commented_path, "wb") as file: # Lưu lại ID những post đã comment
                                    pickle.dump(commented_id, file)
                                return
                            commented_id.add(postID)
                            countSpam += 1
                        if len(commented_id) == int(self.post_number):
                            break
                    except:
                        pass
                with open(commented_path, "wb") as file: # Lưu lại ID những post đã comment
                    pickle.dump(commented_id, file)
            if countSpam >= spam_limit:
                self.signals.finished.emit()
                self.signals.log.emit("SPAM: Đã spam " + str(countSpam) + " posts! Hãy nghỉ ngơi")
                self._stop = True
                return
            if countReload % 3 == 0:
                second = random.randint(120, 180)
                while second > 0:
                    self.signals.log.emit("SPAM: đợi bài đăng mới, đã spam " + str(countSpam) + " posts, count down " + str(second) + " s")
                    time.sleep(1)
                    second -= 1
                self.signals.log.emit("SPAM: Đang spam các post trong news feed")
            time.sleep(random.randint(self.scan_delay[0],self.scan_delay[len(self.scan_delay)-1]))
    
    def check_open_post(self):
        div = self.driver.find_element(By.XPATH, "//div[@role='banner']/following-sibling::div[1]")
        if div.get_attribute("class") == "x9f619 x1n2onr6 x1ja2u2z":
            return False
        else: return True
            
    def set_stop(self, value: bool):
        self._stop = value