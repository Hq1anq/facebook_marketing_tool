import requests
import threading
from PySide6.QtCore import QObject, Signal, Slot, QRunnable, QThreadPool
from src.manager import DriverManager

class CheckSignals(QObject):
    success = Signal(dict, str) # success(sw_options, protocol)
    error = Signal(str)
class CheckWorker(QRunnable):
    class SingleProxyCheck(QRunnable):
        def __init__(self, protocol_name, proxies_dict, url, parent_worker: CheckWorker):
            super().__init__()
            self.protocol_name = protocol_name
            self.proxies_dict = proxies_dict
            self.url = url
            self.parent_worker = parent_worker

        @Slot()
        def run(self):
            try:
                response = requests.get("http://httpbin.io/ip", proxies=self.proxies_dict, timeout=10)
                if response.status_code == 200:
                    sw_options = {
                        'proxy': {
                            'http': self.url,
                            'https': self.url,
                            'no_proxy': 'localhost,127.0.0.1'
                        }
                    }
                    self.parent_worker._handle_success(sw_options, self.protocol_name)
                else:
                    self.parent_worker._handle_error()
            except Exception as e:
                self.parent_worker._handle_error()

    def __init__(self):
        super().__init__()
        self.signals = CheckSignals()
        self.lock = threading.Lock()
        self.reset_state()

    def reset_state(self):
        self.pending_tasks = 2
        self.success_emitted = False

    def setup(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    @Slot()
    def run(self):
        self.reset_state()
        try:
            auth = f"{self.username}:{self.password}@" if self.username and self.password else ""
            socks5_url = f"socks5://{auth}{self.ip}:{self.port}"
            http_url = f"http://{auth}{self.ip}:{self.port}"
            
            proxies_socks5 = {"http": socks5_url, "https": socks5_url}
            proxies_http = {"http": http_url, "https": http_url}
            
            checker_socks5 = self.SingleProxyCheck("SOCKS5", proxies_socks5, socks5_url, self)
            checker_http = self.SingleProxyCheck("HTTP", proxies_http, http_url, self)
            
            # Sử dụng QThreadPool của PySide6
            pool = QThreadPool.globalInstance()

            pool.start(checker_socks5)
            pool.start(checker_http)
            
        except Exception as e:
            self.signals.error.emit(f"Lỗi hệ thống")
            print(str(e))

    def _handle_success(self, sw_options, protocol):
        with self.lock:
            if self.success_emitted:
                return
            self.success_emitted = True
            
        self.signals.success.emit(sw_options, protocol)

    def _handle_error(self):
        with self.lock:
            if self.success_emitted:
                return
            self.pending_tasks -= 1
            
            if self.pending_tasks == 0:
                self.signals.error.emit("Proxy không hoạt động")

class AddSignal(QObject):
    success = Signal()
    error = Signal(str)
class AddWorker(QRunnable):

    def __init__(self, driver_manager: DriverManager):
        super().__init__()
        self.ip = ''
        self.driver_manager = driver_manager
        self.signals = AddSignal()
    
    def setup(self, ip: str):
        self.ip = ip

    @Slot()
    def run(self):
        try:
            if not self.driver_manager.setup_driver():
                self.signals.error.emit("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
                return
            
            self.driver_manager.get("http://httpbin.io/ip")
            
            self.driver_manager.wait_for_url_contains("") # Full loaded
                
            if self.ip in self.driver_manager.driver.page_source:
                self.signals.success.emit()
            else:
                self.signals.error.emit("Fail: IP driver không trùng khớp!")

        except Exception as e:
            self.signals.error.emit(f"Lỗi khi gắn proxy")
            print(str(e))
