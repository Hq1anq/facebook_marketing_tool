from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from PySide6.QtCore import QRunnable, QObject, Signal, Slot

import json, pyotp, time

from src.manager import DriverManager

class Signals(QObject):
    loading = Signal(str)
    error = Signal(str)
    cookie_output = Signal(str)
    finished = Signal(str)
class Login(QRunnable):
        
    def __init__(self, driver_manager: DriverManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.signals = Signals()
    
    def setup(self, cookie: str, username: str, password: str, twofa: str, type_login: str):
        self.cookie = cookie
        self.username = username
        self.password = password
        self.twoFA = twofa
        self.type_login = type_login
        
    @Slot()
    def run(self):
        if not self.driver_manager.setup_driver():
            self.signals.error.emit("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            return
        if self.driver_manager.check_login():
            profile_name = self.get_profile_name()
            self.signals.finished.emit(profile_name)
            return
            
        self.driver = self.driver_manager.driver
        self.driver.set_window_size(800, 700)
        self.driver.set_window_position(0, 0)
        login_status = self.login()
        if login_status == "Đăng nhập thành công":
            profile_name = self.get_profile_name()
            self.signals.finished.emit(profile_name)
        else:
            self.signals.error.emit(login_status)
    
    def login(self) -> str:
        self.driver_manager.jump_to_facebook()
        if self.driver_manager.check_login():
            return "Đăng nhập thành công"
        if self.type_login == "cookie":
            self.cookie = self.format_cookie(self.cookie)
            self.add_cookie(self.cookie)
            self.driver.refresh()
            self.driver_manager.wait_for_url_contains("") # full loaded
            if not self.driver_manager.check_login():
                return "Sai cookie đăng nhập, hãy thử cách khác..."
            else:
                return "Đăng nhập thành công"

        self.driver_manager.get("https://www.facebook.com/login?locale=en_US")
        email_field = self.driver_manager.wait_for_element(by=By.NAME, value="email")
        self.driver_manager.human_type(email_field, self.username, delay=0.1)
        
        pass_field = self.driver_manager.wait_for_element(by=By.NAME, value="pass")
        self.driver_manager.human_type(pass_field, self.password, delay=0.14)
        
        time.sleep(0.8)  # Đợi một chút trước khi nhấn nút đăng nhập
        login_btn = self.driver_manager.wait_for_element(by=By.XPATH, value="//div[@aria-label='Log In']")
        if login_btn is None:
            return "Không tìm thấy nút đăng nhập"
        login_btn.click()

        self.driver_manager.wait_for_url_contains("") # page full loaded
        time.sleep(5)
        if self.driver_manager.check_login():
            return "Đăng nhập thành công"
        else:
            try:
                # Chọn xác thực cách khác
                self.driver_manager.wait_for_url_contains("two_step_verification")
                try_another_btn = self.driver_manager.wait_for_clickable_element(By.XPATH, "//div[@role='button']")
                if try_another_btn is None:
                    raise Exception("Không tìm thấy nút 'Thử cách khác'")
                self.driver_manager.click_element(try_another_btn)
                
                # Chọn xác thực bằng ứng dụng
                authen_use_app = self.driver_manager.wait_for_element(By.XPATH, "(//label[@class='x1lliihq x1n2onr6 x1exlly7 x1e7cf47 x44cjkt x1dygckn'])[2]")
                if authen_use_app is None:
                    raise Exception("Không tìm thấy nút 'Xác thực bằng ứng dụng'")
                self.driver_manager.click_element(authen_use_app)
            
                # Chọn tiếp tục
                continue_button = self.driver_manager.wait_for_clickable_element(By.XPATH, "//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w xeuugli x1iyjqo2 xs83m0k xdl72j9 x1yrsyyn x1icxu4v x10b6aqq x25sj25']//div[@role='button']")
                if continue_button is None:
                    raise Exception("Không tìm thấy nút 'Tiếp tục'")
                self.driver_manager.click_element(continue_button)
            except:
                return "Đăng nhập thất bại, sai username/password hoặc dính captcha"
            
            # Nhập code 2fa
            totp = pyotp.TOTP(self.twoFA.replace(" ", "").upper())
            code = totp.now()
            code_input = self.driver_manager.wait_for_element(By.CSS_SELECTOR, ".xtpw4lu")
            if code_input is None:
                return "Không tìm thấy ô nhập mã 2FA"
            code_input.send_keys(code)
            submit_btn = self.driver_manager.wait_for_clickable_element(By.XPATH, "//div[@class='xod5an3 xg87l8a']//div[@role='button']")
            if submit_btn is None:
                return "Không tìm thấy nút xác nhận 2FA"
            submit_btn.click()
            
            self.driver_manager.wait_for_url_contains("remember_browser")
            time.sleep(5)
            if self.driver_manager.jump_to_facebook():
                return "Đăng nhập thành công"
            else:
                return "Đăng nhập thất bại, sai mã 2fa"

    def get_profile_name(self):
        try:
            self.driver_manager.get("https://www.facebook.com/me")
            profile_name = self.driver_manager.wait_for_element(By.XPATH, "//div[@class='x78zum5 xdt5ytf x1wsgfga x9otpla']//h1").text.strip()
            return profile_name
        except (NoSuchElementException, Exception) as e:
            print(f"Error getting username: {e}")
            return None
    
    def format_cookie(self, cookie_string: str) -> str:
        """
        Convert multiple cookie formats (JSON, Tabular, Standard) to standard "name=value; name=value" format.
        """
        
        if not cookie_string:
            return ""
            
        cookie_string = cookie_string.strip()
        cookies = []
        parsed_names = set()

        # 1. Thử phân tích dạng JSON (Từ các Extension như EditThisCookie, J2Team)
        try:
            cookie_list = json.loads(cookie_string)
            if isinstance(cookie_list, list):
                for item in cookie_list:
                    if isinstance(item, dict) and 'name' in item and 'value' in item:
                        name = str(item['name']).strip()
                        value = str(item['value']).strip()
                        if name and name not in parsed_names:
                            cookies.append(f"{name}={value}")
                            parsed_names.add(name)
                if cookies:
                    return "; ".join(cookies)
        except json.JSONDecodeError:
            pass

        # 2. Xử lý dạng văn bản (Bảng DevTools hoặc chuỗi chuẩn)
        lines = cookie_string.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Kiểm tra xem có phải dạng chuẩn name=value không (điển hình thường có "=")
            if '=' in line:
                for part in line.split(';'):
                    part = part.strip()
                    if not part:
                        continue
                    if '=' in part:
                        name, value = part.split('=', 1)
                        name = name.strip()
                        value = value.strip()
                        if name not in parsed_names:
                            cookies.append(f"{name}={value}")
            else: # Trường hợp Dạng bảng: Dùng `.split()` để tách bằng bất kỳ khoảng trắng liên tiếp nào (Space, Tab, hỗn hợp)
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0].strip()
                    value = parts[1].strip()
                    
                    # Bỏ qua các tiêu đề cột hoặc các giá trị rỗng bị đẩy nhầm cột lùi lên
                    if name.lower() in ['name', 'domain', 'path', 'expires', 'size']:
                        continue
                    if value.startswith('.') or value == '/' or value.lower() == 'session':
                        continue
                    
                    if name and name not in parsed_names:
                        cookies.append(f"{name}={value}")
                        parsed_names.add(name)

        return "; ".join(cookies)

    def get_cookie(self):
        if self.driver_manager.check_login():
            try:
                self.driver = self.driver_manager.driver
                c_user = self.driver.get_cookie("c_user")
                fr = self.driver.get_cookie("fr")
                sb = self.driver.get_cookie("sb")
                xs = self.driver.get_cookie("xs")
                datr = self.driver.get_cookie("datr")
                
                if not all([c_user, fr, sb, xs, datr]):
                    print("Warning: One or more cookies are missing")
                    return None
                
                return "c_user=%s; fr=%s; sb=%s; xs=%s; datr=%s"%(
                    c_user["value"],
                    fr["value"],
                    sb["value"],
                    xs["value"],
                    datr["value"]
                )
            except (TypeError, KeyError) as e:
                print(f"Error getting cookies: {e}")
                return None
        else:
            return None

    def add_cookie(self, cookie_string: str):
        formatted_cookie = self.format_cookie(cookie_string)
        self.signals.cookie_output.emit(cookie_string)
        cookies = [cookie.strip() for cookie in formatted_cookie.split(';') if cookie.strip()]
        for cookie in cookies:
            if '=' in cookie:
                name, value = cookie.split('=', 1)
                self.driver.add_cookie({
                    'name': name.strip(),
                    'value': value.strip()
                })