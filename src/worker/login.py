from selenium.webdriver.common.by import By
from PySide6.QtCore import QRunnable, QObject, Signal, Slot

import pyotp, time

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
            try:
                # Chọn xác thực cách khác
                try_another_btn = self.driver_manager.wait_for_clickable_element(By.CSS_SELECTOR, ".xjbqb8w")
                self.driver_manager.click_element(try_another_btn)
                
                # Chọn xác thực bằng ứng dụng
                authen_use_app = self.driver_manager.wait_for_element(By.XPATH, "(//label[@class='x1lliihq x1n2onr6 x1exlly7 x1e7cf47 x44cjkt x1dygckn'])[2]")
                self.driver_manager.click_element(authen_use_app)
            
                # Chọn tiếp tục
                continue_button = self.driver_manager.wait_for_clickable_element(By.XPATH, "//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w xeuugli x1iyjqo2 xs83m0k xdl72j9 x1yrsyyn x1icxu4v x10b6aqq x25sj25']//div[@role='button']")
                self.driver_manager.click_element(continue_button)
            except:
                return "Đăng nhập thất bại, sai username/password hoặc dính captcha"
            
            # Nhập code 2fa
            totp = pyotp.TOTP(self.twoFA.replace(" ", "").upper())
            code = totp.now()
            self.driver_manager.wait_for_element(By.CSS_SELECTOR, ".xtpw4lu").send_keys(code)
            self.driver_manager.wait_for_clickable_element(By.XPATH, "//div[@class='xod5an3 xg87l8a']//div[@role='button']").click()
            
            #Chờ xác nhận (hiện dialog lưu thông tin đăng nhập)
            self.driver_manager.wait_for_element(By.XPATH, "div[@role='dialog']")
            
            if self.driver_manager.jump_to_facebook():
                return "Đăng nhập thành công"
            else:
                return "Đăng nhập thất bại, sai mã 2fa"
        
    def add_cookie(self, cookie_string: str):
        cookies = [cookie.strip() for cookie in cookie_string.split(';')]
        for cookie in cookies:
            name, value = cookie.split('=', 1)
            self.driver.add_cookie({'name': name, 'value': value})