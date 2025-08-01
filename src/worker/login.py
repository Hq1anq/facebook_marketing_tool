from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PySide6.QtCore import QRunnable, QObject, Signal, Slot

from src.manager import DriverManager, DataManager

class Login(QRunnable):
    class Signals(QObject):
        log = Signal(str)
        cookie_output = Signal(str)
        profile_name = Signal(str)
        hide_loginFrame = Signal()
        
    def __init__(self, driver_manager: DriverManager, data_manager: DataManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.data_manager = data_manager
        self.signals = self.Signals()
        
    @Slot()
    def run(self):
        self.cookies: str = self.data_manager.data["GET"]["LOGIN"]["cookies"]
        self.driver_manager.jump_to_facebook()
        if not self.driver_manager.setup_driver():
            self.signals.log.emit("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            return
        self.driver = self.driver_manager.driver
        self.driver_manager.jump_to_facebook()
        if not self.driver_manager.is_login:
            if self.cookies != "":
                self.driver_manager.add_cookie(self.cookies)
                self.driver.refresh()
                self.driver_manager.wait_for_element(By.ID, "facebook")
                if not self.driver_manager.check_login():
                    self.signals.log.emit("Chưa đăng nhập, sai cookie")
                    return
            else:
                self.driver.set_window_size(800, 700)
                self.driver.set_window_position(0, 0)
                login_status = self.login()
                self.signals.log.emit(login_status)
                if login_status ==  "Đăng nhập thành công":
                    self.signals.hide_loginFrame.emit()
        if self.driver_manager.is_login:
            self.set_profile()
            self.signals.log.emit("Đăng nhập thành công")
            self.signals.hide_loginFrame.emit()
            return
    
    def login(self) -> str:
        try:
            self.driver.find_element(by=By.ID, value="facebook")
        except:
            return "Lỗi load Facebook"
        cookie_string = self.data_manager.data["GET"]["LOGIN"]["cookies"]
        if cookie_string != "":
            self.add_cookie(cookie_string)
            self.driver.refresh()
            self.driver_manager.wait_for_element(By.ID, "facebook")
            if self.driver_manager.check_login(): return "Đăng nhập thành công"
        username = self.data_manager.data["GET"]["LOGIN"]["username"]
        password = self.data_manager.data["GET"]["LOGIN"]["password"]
        twoFA = self.data_manager.data["GET"]["LOGIN"]["2fa"]
        if username == "" or password == "":
            return "Thiếu thông tin đăng nhập"
        else:
            self.driver_manager.wait_for_element(by=By.ID, value="email").send_keys(username)
            self.driver_manager.wait_for_element(by=By.ID, value="pass").send_keys(password)
            self.driver_manager.wait_for_element(by=By.ID, value="loginbutton").click()
            if self.driver_manager.check_login():
                self.set_profile()
                return "Đăng nhập thành công"
            else:
                actions = ActionChains(self.driver)
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
                self.driver.execute_script('window.open("https://2fa.live/tok/'+twoFA+'")')
                self.driver.switch_to.window(self.driver.window_handles[1])
                code = self.driver.find_element(By.TAG_NAME,"pre").text.split(':"')[1][:6]
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                # Nhập code 2fa
                self.driver.find_element(By.ID, ":r9:").send_keys(code)
                self.driver.find_element(By.CSS_SELECTOR, ".xtvsq51 > .x6s0dn4").click()
                # Lưu đăng nhập
                if "remember_browser" in self.driver.current_url:
                    self.driver.find_element(By.CSS_SELECTOR, ".xtk6v10 > .x1lliihq").click()
                if ("Bạn bè" in self.driver.page_source) or ("Friends" in self.driver.page_source):
                    self.set_profile()
                    return "Đăng nhập thành công"
    
    def get_cookies(self):
        self.driver_manager.jump_to_facebook()
        if self.driver_manager.is_login:
            cookies = "c_user=%s; fr=%s; sb=%s; xs=%s; datr=%s"%(
                self.driver.get_cookie("c_user")["value"],
                self.driver.get_cookie("fr")["value"],
                self.driver.get_cookie("sb")["value"],
                self.driver.get_cookie("xs")["value"],
                self.driver.get_cookie("datr")["value"]
            )
            self.signals.cookie_output.emit(cookies)
            self.signals.log.emit("Đã login và lấy cookies")
            profile_name = self.get_username()
            self.signals.profile_name.emit(profile_name)
        else:
            self.driver.set_window_size(800, 700)
            self.driver.set_window_position(0, 0)
            login_status = self.login()
            if login_status == "Đăng nhập thành công":
                cookies = "c_user=%s; fr=%s; sb=%s; xs=%s; datr=%s"%(
                    self.driver.get_cookie("c_user")["value"],
                    self.driver.get_cookie("fr")["value"],
                    self.driver.get_cookie("sb")["value"],
                    self.driver.get_cookie("xs")["value"],
                    self.driver.get_cookie("datr")["value"]
                )
                self.data_manager.data["GET"]["LOGIN"]["cookies"] = cookies
                self.signals.cookie_output.emit(cookies)
                self.signals.log.emit("Đã login và lấy cookies")
            else:
                self.signals.log.emit(login_status)
    
    def get_userID(self):
        profile_name = self.driver.find_element(By.XPATH, '//a[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xe8uvvx xdj266r xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1n2onr6 x87ps6o x1lku1pv x1a2a7pz x78zum5 x1emribx"]')
        return profile_name.get_attribute("href").split("id=")[1]
    
    def get_username(self):
        profile_name = self.driver.find_element(By.XPATH, '//span[@id=":Rbadakl6illkqismipapd5aq:"]/span').text
        return profile_name
    
    def set_profile(self):
        profile_name = self.get_username()
        self.data_manager.data["GET"]["LOGIN"]["profile name"] = profile_name
        self.signals.profile_name.emit(profile_name)
        
    def add_cookie(self, cookie_string: str):
        cookies = [cookie.strip() for cookie in cookie_string.split(';')]
        for cookie in cookies:
            name, value = cookie.split('=', 1)
            self.driver.add_cookie({'name': name, 'value': value})