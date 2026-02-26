from PySide6.QtCore import Qt, QSize, QThreadPool, QTimer
from PySide6.QtGui import QIcon

from src.manager import DataManager, DriverManager
from src.gui.widget.ui_interface import Ui_MainWindow
from src.worker.proxy import CheckWorker, AddWorker

class ProxyUI:
    def __init__(self, ui: Ui_MainWindow, data_manager: DataManager, driver_manager: DriverManager):
        self.ui = ui
        self.data_manager = data_manager
        self.driver_manager = driver_manager
        self.check_res = [None, None]
        self.ip = None
        self._is_adding_proxy_pending = False
        
        # Instantiate worker
        self.check_worker = CheckWorker()
        self.add_worker = AddWorker(self.driver_manager)

        self.check_worker.signals.success.connect(self.on_check_success)
        self.check_worker.signals.error.connect(self.on_check_error)
        self.check_worker.signals.log.connect(self.ui.status.setText)
        self.check_worker.setAutoDelete(False)
        
        self.add_worker.signals.success.connect(self.on_add_success)
        self.add_worker.signals.error.connect(self.on_add_error)
        self.add_worker.signals.log.connect(self.ui.status.setText)
        self.add_worker.setAutoDelete(False)
        self.setup_connections()

    def on_check_success(self, sw_options, protocol):
        self.check_res = [self.ip, sw_options]
        self.ui.status.setSuccess(f"Proxy {protocol} đang hoạt động")
        self.driver_manager.set_proxy(sw_options)
        
        if self._is_adding_proxy_pending:
            self._is_adding_proxy_pending = False
            self._start_add_worker()
        else:
            self.on_finished()

    def on_check_error(self, err_msg):
        self.check_res = [self.ip, None]
        self.ui.status.setError(err_msg)
        self.driver_manager.set_proxy({})
        self._is_adding_proxy_pending = False
        self.on_finished()
        
    def on_add_success(self):
        self.ui.status.setSuccess("Gắn proxy thành công!")
        icon = QIcon()
        icon.addFile(u":/icons/icons/proxyOK.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ui.btn_proxy.setIcon(icon)
        self.on_finished()

    def on_add_error(self, err_msg):
        self.ui.status.setError(err_msg)
        icon = QIcon()
        icon.addFile(u":/icons/icons/proxyERR.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ui.btn_proxy.setIcon(icon)
        self.on_finished()

    def on_finished(self):
        self.ui.addProxyBtn.setEnabled(True)
        self.ui.checkProxyBtn.setEnabled(True)

    def setup_connections(self):
        self.ui.proxyDetailCheckbox.stateChanged.connect(self.changeProxyInputMethod)
        self.ui.checkProxyBtn.clicked.connect(self.check_proxy)
        self.ui.addProxyBtn.clicked.connect(self.add_proxy)
    
    def check_proxy(self):
        try:
            self.save_data()
        except SyntaxError as e:
            self.on_check_error(str(e))
            return
        ip = self.data_manager.data["PROXY"]["ip"]
        port = self.data_manager.data["PROXY"]["port"]
        username = self.data_manager.data["PROXY"]["username"]
        password = self.data_manager.data["PROXY"]["password"]

        self.ui.status.setText("Đang kiểm tra proxy (Socks5/HTTP)...")
        self.ui.addProxyBtn.setEnabled(False)
        self.ui.checkProxyBtn.setEnabled(False)
        
        self.check_worker.setup(ip, port, username, password)
        QThreadPool.globalInstance().start(self.check_worker)

    def add_proxy(self):
        try:
            self.save_data()
        except SyntaxError as e:
            self.on_check_error(str(e))
            return
            
        if self.check_res[0] == self.ip and self.check_res[1]:
            self.driver_manager.set_proxy(self.check_res[1])
            self._start_add_worker()
        else:
            self._is_adding_proxy_pending = True
            self.check_proxy()
            
    def _start_add_worker(self):
        self.ui.addProxyBtn.setEnabled(False)
        self.ui.checkProxyBtn.setEnabled(False)
        self.add_worker.setup(self.ip)
        QThreadPool.globalInstance().start(self.add_worker)
    
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
        
        self.ip = ip