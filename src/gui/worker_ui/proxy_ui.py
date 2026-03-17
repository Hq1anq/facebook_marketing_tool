from PySide6.QtCore import Qt, QSize, QThreadPool, QTimer
from PySide6.QtWidgets import QLabel

import src.settings as settings
from src.manager import DataManager, DriverManager
from src.gui.widget.ui_interface import Ui_MainWindow
from src.worker import ProxyTestWorker
import time

class ProxyUI:
    def __init__(self, ui: Ui_MainWindow, data_manager: DataManager, driver_manager: DriverManager):
        self.ui = ui
        self.data_manager = data_manager
        self.driver_manager = driver_manager
        
        # Instantiate worker
        self.proxy_worker = ProxyTestWorker()
        self.proxy_worker.signals.result.connect(self.on_proxy_tested)
        self.proxy_worker.signals.error.connect(lambda error_msg: self.ui.status.setError(error_msg))
        self.proxy_worker.signals.message.connect(lambda msg: self.ui.status.setText(msg))
        
        def on_finished():
            self.ui.addProxyBtn.setEnabled(True)
            self.ui.checkProxyBtn.setEnabled(True)
            
        self.proxy_worker.signals.finished.connect(on_finished)
        
        self.setup_connections()

    def setup_connections(self):
        self.ui.proxyDetailCheckbox.stateChanged.connect(self.changeProxyInputMethod)
        self.ui.checkProxyBtn.clicked.connect(self.check_proxy)
        # self.ui.addProxyBtn.clicked.connect(self.apply_proxy)
    
    def check_proxy(self):
        try:
            self.save_data()
        except SyntaxError as e:
            self.on_proxy_error(str(e))
            return
        ip = self.data_manager.data["PROXY"]["ip"]
        port = self.data_manager.data["PROXY"]["port"]
        username = self.data_manager.data["PROXY"]["username"]
        password = self.data_manager.data["PROXY"]["password"]

        if not ip or not port:
            self.ui.status.setText("Vui lòng nhập đầy đủ IP và Port proxy")
            self.ui.status.setStyleSheet("color: red;")
            # Clear proxy from runtime if fields are empty
            self.driver_manager.set_proxy({})
            return

        self.ui.status.setText("Đang kiểm tra proxy (Socks5/HTTP)...")
        self.ui.addProxyBtn.setEnabled(False)
        self.ui.checkProxyBtn.setEnabled(False)

        self.proxy_worker.setup(ip, port, username, password)
        self.proxy_worker.run()

    def on_proxy_tested(self, sw_options, protocol):
        self.ui.status.setSuccess(f"Proxy {protocol} đang hoạt động")
        self.driver_manager.set_proxy(sw_options)
        
    def on_proxy_error(self, err_msg):
        self.ui.status.setError(err_msg)
    
    def changeProxyInputMethod(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.proxyInputDetailFrame.show()
            self.ui.proxyInput.hide()
            self.ui.fullProxyLabel.hide()
        else:
            self.ui.proxyInputDetailFrame.hide()
            self.ui.proxyInput.show()
            self.ui.fullProxyLabel.show()

    def load_data(self):
        ip = self.data_manager.data["PROXY"]["ip"]
        port = self.data_manager.data["PROXY"]["port"]
        username = self.data_manager.data["PROXY"]["username"]
        password = self.data_manager.data["PROXY"]["password"]
        
        if (any([ip, port, username, password])):
            self.ui.proxyIpInput.setText(ip)
            self.ui.proxyPortInput.setText(port)
            self.ui.proxyUserInput.setText(username)
            self.ui.proxyPassInput.setText(password)
            self.ui.proxyInput.setText(f"{ip}:{port}:{username}:{password}")
    
    def save_data(self):
        ip, port, username, password = "", "", "", ""
        if self.ui.proxyDetailCheckbox.isChecked():
            ip = self.ui.proxyIpInput.text()
            port = self.ui.proxyPortInput.text()
            username = self.ui.proxyUserInput.text()
            password = self.ui.proxyPassInput.text()
        else:
            info = self.ui.proxyInput.text().split(":")
            match len(info):
                case 4:
                    ip, port, username, password = info
                case 2:
                    ip, port = info
                case _:
                    raise SyntaxError("Sai định dạng Proxy")

        self.data_manager.data["PROXY"]["ip"] = ip
        self.data_manager.data["PROXY"]["port"] = port
        self.data_manager.data["PROXY"]["username"] = username
        self.data_manager.data["PROXY"]["password"] = password