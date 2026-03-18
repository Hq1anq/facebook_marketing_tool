from PySide6.QtCore import Qt, QSize

import src.settings as settings
from src.manager import DataManager
from src.gui.widget.ui_interface import Ui_MainWindow

class ProxyUI:
    def __init__(self, ui: Ui_MainWindow, data_manager: DataManager):
        self.ui = ui
        self.data_manager = data_manager
        
        self.setup_connections()

    def setup_connections(self):
        self.ui.btn_proxy.clicked.connect(self.changeStatusProxy)
        self.ui.proxyCheckBox.clicked.connect(lambda: self.ui.btn_proxy.click())
        self.ui.proxyDetailCheckbox.stateChanged.connect(self.changeProxyInputMethod)
    
    def changeStatusProxy(self):
        if self.ui.btn_proxy.isChecked():
            self.ui.proxyCheckBox.setCheckState(Qt.CheckState.Checked)
            self.ui.proxyFrame.show()
        else:
            self.ui.proxyCheckBox.setCheckState(Qt.CheckState.Unchecked)
            self.ui.proxyFrame.hide()
    
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
                    raise Exception("Không thể lưu do sai định dạng Proxy")

        self.data_manager.data["PROXY"]["ip"] = ip
        self.data_manager.data["PROXY"]["port"] = port
        self.data_manager.data["PROXY"]["username"] = username
        self.data_manager.data["PROXY"]["password"] = password