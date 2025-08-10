from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class DriverManager:
    def __init__(self, chrome_path: str):
        self.driver = None
        self.chrome_path = chrome_path
        self.language = "vi"
        self.friend_str = "Bạn bè"
        self.message_str = "Nhắn tin"
        self.post = "Đăng"
        self.comment_aria = "Viết bình luận"
        self.comment_ok = "Bình luận"
        self.no_comment = "tắt tính năng bình luận"
        self.add_image = "Ảnh/video"
        self.close_chat_str = "Đóng đoạn chat"
        self.close_post = "Đóng"
        self.error_message = ["Bạn hiện không xem được nội dung này", "Trang này không hiển thị"]

    def setup_driver(self) -> bool:
        try:
            self.driver.title
            return True
        except:
            options = Options()
            options.add_experimental_option("detach", True) # Giữ cửa sổ mở
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            options.add_argument("user-data-dir=" + self.chrome_path) # Chỉ định profile cho browser
            options.add_argument("--disable-notifications")
            options.add_argument("--window-size=1130,500")
            try:
                self.driver = webdriver.Chrome(options=options)
                self.actions = ActionChains(self.driver)
                self.wait20 = WebDriverWait(self.driver, 20)
                self.wait15 = WebDriverWait(self.driver, 15)
                self.wait10 = WebDriverWait(self.driver, 10)
                self.wait5 = WebDriverWait(self.driver, 5)
            except:
                return False
            return True

    def adjust_language(self):
        self.language = self.driver.find_element(By.XPATH, "//html").get_attribute('lang')
        if self.language != "en":
            self.message_str = "Nhắn tin"
            self.post = "Đăng"
            self.comment_aria = "Viết bình luận"
            self.comment_ok = "Bình luận"
            self.no_comment = "tắt tính năng bình luận"
            self.add_image = "Ảnh/video"
            self.close_chat_str = "Đóng đoạn chat"
            self.close_post = "Đóng"
            self.friend_str = "Bạn bè"
            self.error_message = ["Bạn hiện không xem được nội dung này", "Trang này không hiển thị"]
        else:
            self.message_str = "Message"
            self.post = "Post"
            self.comment_aria = "Leave a comment"
            self.comment_ok = "Comment"
            self.no_comment = "turned off commenting"
            self.add_image = "Photo/video"
            self.close_chat_str = "Close chat"
            self.close_post = "Close"
            self.friend_str = "Friends"
            self.error_message = ["This content isn't available right now", "This Page Isn't Available"]
    
    def handle_chat_close(self):
        script = f"""
        let closeButtons = document.evaluate(
            "//div[@aria-label='{self.close_chat_str}']",
            document,
            null,
            XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
            null
        );

        for (let i = 0; i < closeButtons.snapshotLength; i++) {{
            closeButtons.snapshotItem(i).click();
        }}
        """

        # Execute the JavaScript in the browser
        self.driver.execute_script(script)
    
    def get(self, url):
        if self.driver is not None:
            self.driver.get(url)
    
    def get_username(self):
        profile_name = self.driver.find_element(By.XPATH, '//span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6"]').text
        return profile_name

    def get_userID(self):
        script_text = self.driver.find_element(
            By.CSS_SELECTOR, "head > script#__eqmc"
        ).get_attribute("innerHTML")

        user_id = script_text.split("__user=")[1].split("&")[0]
        
        return user_id
    
    def check_login(self) -> bool:
        self.is_login = self.friend_str in self.driver.page_source
        return self.is_login
    
    def jump_to_facebook(self) -> bool:
        self.driver.get("https://www.facebook.com/login")
        self.adjust_language()
        self.check_login()
        return self.is_login
    
    def get_cookies(self):
        if self.is_login:
            return "c_user=%s; fr=%s; sb=%s; xs=%s; datr=%s"%(
                self.driver.get_cookie("c_user")["value"],
                self.driver.get_cookie("fr")["value"],
                self.driver.get_cookie("sb")["value"],
                self.driver.get_cookie("xs")["value"],
                self.driver.get_cookie("datr")["value"]
            )
        else:
            return None
    
    def add_cookie(self, cookie_string: str):
        cookies = [cookie.strip() for cookie in cookie_string.split(';')]
        for cookie in cookies:
            name, value = cookie.split('=', 1)
            self.driver.add_cookie({'name': name, 'value': value})

    def close(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
    
    def scroll(self, scroll_times: int, timeout: float = 5.0) -> None:
        for i in range(scroll_times):
            try:
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script(f"window.scrollTo(0, {last_height - 800});")
                
                # Use explicit wait until scrollHeight increases
                WebDriverWait(self.driver, timeout).until(
                    lambda d: d.execute_script("return document.body.scrollHeight") > last_height
                )
            except:
                print(f"[Scroll {i+1}] No new content loaded after scrolling.")
                break  # Stop if no new content is loaded (e.g., reached end of page)
    
    def scroll_to_bottom(self, max_scrolls: int = 30, timeout: float = 5.0) -> None:
        """Scroll until no new content is loaded or max_scrolls is reached."""
        for i in range(max_scrolls):
            try:
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script(f"window.scrollTo(0, {last_height - 500});")

                WebDriverWait(self.driver, timeout).until(
                    lambda d: d.execute_script("return document.body.scrollHeight") > last_height
                )
            except:
                print(f"[Scroll {i+1}] No more new content.")
                break
    
    def wait_for_element(self, by, value):
        try:
            return self.wait15.until(EC.presence_of_element_located((by, value)))
        except Exception as e:
            print(f"Error waiting for element: {e}")
            return None
        
    def click_element(self, element):
        self.actions.click(element).perform()