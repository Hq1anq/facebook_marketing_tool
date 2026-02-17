from PySide6.QtCore import Qt, QSize

import src.settings as settings
from src.manager import DataManager
from src.gui.widget.ui_interface import Ui_MainWindow
from src.gui.styles import BUTTON_STYLE

class LoginUI:
    def __init__(self, ui: Ui_MainWindow, data_manager: DataManager):
        self.ui = ui
        self.data_manager = data_manager
        
        self.setup_connections()

    def setup_connections(self):
        self.ui.btn_reload_loginMethod.clicked.connect(self.load_data)
        
        # Login Page
        self.ui.methodComboBox.activated.connect(self.toggle_login_method)
        self.ui.loginDetail.stateChanged.connect(self.toggle_login_detail)
        self.ui.twoFACheckBox.stateChanged.connect(self.toggle_use_2fa)
    
    def toggle_login_method(self):
        match self.ui.methodComboBox.currentText():
            case "Username|Password|2fa":
                self.ui.loginMethodStacked.setCurrentWidget(self.ui.useUserPass)
            case _:
                self.ui.loginMethodStacked.setCurrentWidget(self.ui.useCookie)
    
    def toggle_login_detail(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.fullLoginInput.hide()
            self.ui.fullLoginLabel.hide()
            self.ui.loginDetailFrame.show()
            infoGroup = self.ui.fullLoginInput.text().split("|")
            if len(infoGroup) >= 2:
                self.ui.userInput.setText(infoGroup[0])
                self.ui.passInput.setText(infoGroup[1])
            if len(infoGroup) == 3:
                self.ui.twoFAInput.setText(infoGroup[2].replace(" ", ""))
                self.ui.twoFACheckBox.setCheckState(Qt.CheckState.Checked)
            else:
                self.ui.twoFAInput.clear()
                self.ui.twoFACheckBox.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.ui.fullLoginInput.show()
            self.ui.fullLoginLabel.show()
            self.ui.loginDetailFrame.hide()
            if self.ui.twoFACheckBox.checkState() == Qt.CheckState.Checked:
                infoGroup = self.ui.userInput.text()+"|"+self.ui.passInput.text()+"|"+self.ui.twoFAInput.text()
            else:
                infoGroup = self.ui.userInput.text()+"|"+self.ui.passInput.text()
            self.ui.fullLoginInput.setText(infoGroup)
    
    def toggle_use_2fa(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.twoFAInput.show()
            self.ui.fullLoginInput.setText("USER|PASS|2FA")
            self.ui.fullLoginInput.setText(self.ui.userInput.text()+"|"+self.ui.passInput.text()+"|"+self.ui.twoFAInput.text().replace(" ", ""))
        else:
            self.ui.twoFAInput.hide()
            self.ui.fullLoginInput.setText("USER|PASS")
            self.ui.fullLoginInput.setText(self.ui.userInput.text()+"|"+self.ui.passInput.text())

    def load_data(self):
        cookie = self.data_manager.data["LOGIN"]["cookie"]
        username = self.data_manager.data["LOGIN"]["username"]
        password = self.data_manager.data["LOGIN"]["password"]
        twoFA = self.data_manager.data["LOGIN"]["2fa"]
        profile_name = self.data_manager.data["LOGIN"]["profile name"]
        self.ui.cookieInput.setPlainText(cookie)
        self.ui.userInput.setText(username)
        self.ui.passInput.setText(password)
        self.ui.twoFAInput.setText(twoFA)
        if (profile_name):
            self.ui.profileName.setText(profile_name)
            self.ui.profileName.setIconSize(QSize(40, 40))
        else:
            self.ui.profileName.setText("LOGIN")
            self.ui.profileName.setIconSize(QSize(0, 0))
            self.ui.profileName.setStyleSheet(BUTTON_STYLE)

        if self.ui.loginDetail.isChecked():
            if settings.using2FA:
                self.ui.fullLoginInput.setText(username+"|"+password+"|"+twoFA)
            else:
                self.ui.fullLoginInput.setText(username+"|"+password)
    
    def save_data(self):
        if self.ui.getStacked.currentWidget() == self.ui.loginPage:
            username, password, twoFA = "", "", ""
            if self.ui.loginDetail.isChecked():
                info = self.ui.fullLoginInput.text().split("|")
                if len(info) >= 2:
                    username = info[0]
                    password = info[1]
                if len(info) == 3:
                    twoFA = info[2].replace(" ", "")
            else:
                username = self.ui.userInput.text()
                password = self.ui.passInput.text()
                twoFA = self.ui.twoFAInput.text()
            cookie = self.ui.cookieInput.toPlainText()
            self.data_manager.data["LOGIN"]["username"] = username
            self.data_manager.data["LOGIN"]["password"] = password
            self.data_manager.data["LOGIN"]["2fa"] = twoFA
            self.data_manager.data["LOGIN"]["cookie"] = cookie
        if self.ui.profileName.text() != "":
            self.data_manager.data["LOGIN"]["profile name"] = self.ui.profileName.text()