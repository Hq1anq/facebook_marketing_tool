from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PySide6.QtCore import QRunnable, QObject, Signal, Slot

import pyotp

from src.manager import DriverManager, DataManager

class Login(QRunnable):
    class Signals(QObject):
        log = Signal(str)
        cookie_output = Signal(str)
        finished = Signal()
        
    def __init__(self, driver_manager: DriverManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.signals = self.Signals()
    
    def setup(self, cookie: str, username: str, password: str, twofa: str):
        self.cookie = cookie
        self.username = username
        self.password = password
        self.twoFA = twofa
        
    @Slot()
    def run(self):
        self.driver = self.driver_manager.driver
        
        if self.driver_manager.is_login:
            self.signals.finished.emit()
            return
            
        self.driver.set_window_size(800, 700)
        self.driver.set_window_position(0, 0)
        login_status = self.login()
        if login_status == "Đăng nhập thành công":
            self.signals.finished.emit()
        else:
            self.signals.log.emit(login_status)
    
    def login(self) -> str:
        if self.cookie != "":
            self.driver_manager.add_cookie(self.cookie)
            self.driver.refresh()
            self.driver_manager.wait_for_element(By.ID, "facebook")
            if not self.driver_manager.check_login():
                self.signals.log.emit("Sai cookie đăng nhập, đang thử cách khác...")
            else:
                return "Đăng nhập thành công"
        if not (self.username and self.password):
            return "Thiếu thông tin đăng nhập"
        self.driver_manager.wait_for_element(by=By.ID, value="email").send_keys(self.username)
        self.driver_manager.wait_for_element(by=By.ID, value="pass").send_keys(self.password)
        self.driver_manager.wait_for_element(by=By.ID, value="loginbutton").click()
        if self.driver_manager.check_login():
            return "Đăng nhập thành công"
        else:
            actions = self.driver_manager.actions
            element = self.driver.find_element(By.CSS_SELECTOR, "body")
            actions.move_to_element(element).perform()
            # Chọn xác thực cách khác
            self.driver.find_element(By.CSS_SELECTOR, ".x6ikm8r").click()
            # Chọn xác thực bằng ứng dụng
            self.driver.find_element(By.XPATH, "//div[@id=\':r5:\']/div/div[2]").click()
            # Chọn tiếp tục
            actions = ActionChains(self.driver) 
            actions.send_keys(Keys.TAB * 6)
            actions.perform()
            actions.send_keys(Keys.ENTER)
            actions.perform()
            totp = pyotp.TOTP(self.twoFA.replace(" ", "").upper())
            code = totp.now()
            # Nhập code 2fa
            self.driver.find_element(By.ID, ":r9:").send_keys(code)
            self.driver.find_element(By.CSS_SELECTOR, ".xtvsq51 > .x6s0dn4").click()
            # Lưu đăng nhập
            if "remember_browser" in self.driver.current_url:
                self.driver.find_element(By.CSS_SELECTOR, ".xtk6v10 > .x1lliihq").click()
            if self.driver_manager.check_login():
                return "Đăng nhập thành công"
            else:
                return "Đăng nhập thất bại, vui lòng kiểm tra lại thông tin đăng nhập"
        
    def add_cookie(self, cookie_string: str):
        cookies = [cookie.strip() for cookie in cookie_string.split(';')]
        for cookie in cookies:
            name, value = cookie.split('=', 1)
            self.driver.add_cookie({'name': name, 'value': value})