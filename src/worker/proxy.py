import requests
import threading
from PySide6.QtCore import QObject, Signal, Slot, QRunnable, QThreadPool

class SingleProxyChecker(QRunnable):
    def __init__(self, protocol_name, proxies_dict, url, parent_worker):
        super().__init__()
        self.protocol_name = protocol_name
        self.proxies_dict = proxies_dict
        self.url = url
        self.parent_worker = parent_worker

    @Slot()
    def run(self):
        self.parent_worker.signals.message.emit(f"Đang kiểm tra {self.protocol_name}...")
        try:
            response = requests.get("https://ssl-judge2.api.proxyscrape.com/", proxies=self.proxies_dict, timeout=10)
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
                self.parent_worker._handle_error("Status code != 200", self.protocol_name)
        except Exception as e:
            self.parent_worker._handle_error(str(e), self.protocol_name)

class ProxyTestWorker(QObject):
    class Signals(QObject):
        finished = Signal()
        error = Signal(str)
        result = Signal(dict, str) # result(sw_options, protocol)
        message = Signal(str)

    def __init__(self):
        super().__init__()
        self.signals = self.Signals()
        self.lock = threading.Lock()
        self.reset_state()

    def reset_state(self):
        self.pending_tasks = 2
        self.success_emitted = False
        self.errors = []

    def setup(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def run(self):
        self.reset_state()
        try:
            self.signals.message.emit("Khởi tạo kiểm tra Proxy...")
            auth = f"{self.username}:{self.password}@" if self.username and self.password else ""
            socks5_url = f"socks5://{auth}{self.ip}:{self.port}"
            http_url = f"http://{auth}{self.ip}:{self.port}"
            
            proxies_socks5 = {"http": socks5_url, "https": socks5_url}
            proxies_http = {"http": http_url, "https": http_url}
            
            checker_socks5 = SingleProxyChecker("SOCKS5", proxies_socks5, socks5_url, self)
            checker_http = SingleProxyChecker("HTTP", proxies_http, http_url, self)
            
            # Sử dụng QThreadPool của PySide6
            pool = QThreadPool.globalInstance()
            pool.start(checker_socks5)
            pool.start(checker_http)
            
        except Exception as e:
            self.signals.error.emit(f"Lỗi hệ thống: {str(e)}")
            self.signals.finished.emit()

    def _handle_success(self, sw_options, protocol):
        with self.lock:
            if self.success_emitted:
                return
            self.success_emitted = True
            
        self.signals.message.emit(f"Proxy {protocol} khả dụng!")
        self.signals.result.emit(sw_options, protocol)
        self.signals.finished.emit()

    def _handle_error(self, err_msg, protocol):
        with self.lock:
            if self.success_emitted:
                return
            self.errors.append(f"{protocol} - {err_msg}")
            self.signals.message.emit(f"Proxy {protocol} thất bại...")
            self.pending_tasks -= 1
            
            if self.pending_tasks == 0:
                self.signals.error.emit(f"Không kết nối được:\n" + "\n".join(self.errors))
                self.signals.finished.emit()
