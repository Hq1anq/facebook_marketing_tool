from PySide6.QtCore import Qt

import src.settings as settings
from src.manager import DataManager
from src.gui.widget.ui_interface import Ui_MainWindow

class GetUI:
    def __init__(self, ui: Ui_MainWindow, data_manager: DataManager):
        self.ui = ui
        self.data_manager = data_manager
        
        self.setup_connections()

    def setup_connections(self):
        self.ui.getComboBox.activated.connect(self.toggle_get_type)
        self.ui.btn_getReload.clicked.connect(self.load_data)
        
        # Login Page
        self.ui.methodComboBox.activated.connect(self.toggle_login_method)
        self.ui.fullLoginCheckBox.stateChanged.connect(self.toggle_login_detail)
        self.ui.twoFACheckBox.stateChanged.connect(self.toggle_use_2fa)
    
    def toggle_get_type(self):
        if self.ui.getComboBox.currentText() == "LOGIN":
            self.ui.getStacked.setCurrentWidget(self.ui.loginPage)
        else:
            self.ui.getStacked.setCurrentWidget(self.ui.getDataPage)
    
    def toggle_login_method(self):
        if self.ui.methodComboBox.currentText() == "Username|Password|2fa":
            self.ui.loginMethodStacked.setCurrentWidget(self.ui.useUserPass)
        else:
            self.ui.loginMethodStacked.setCurrentWidget(self.ui.useCookie)
    
    def toggle_login_detail(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.fullLoginInput.show()
            self.ui.loginDetailFrame.hide()
            if self.ui.twoFACheckBox.checkState() == Qt.CheckState.Checked:
                infoGroup = self.ui.userInput.text()+"|"+self.ui.passInput.text()+"|"+self.ui.twoFAInput.text()
            else:
                infoGroup = self.ui.userInput.text()+"|"+self.ui.passInput.text()
            self.ui.fullLoginInput.setText(infoGroup)
        else:
            self.ui.fullLoginInput.hide()
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
        cookie = self.data_manager.data["GET"]["LOGIN"]["cookie"]
        username = self.data_manager.data["GET"]["LOGIN"]["username"]
        password = self.data_manager.data["GET"]["LOGIN"]["password"]
        twoFA = self.data_manager.data["GET"]["LOGIN"]["2fa"]
        profile_name = self.data_manager.data["GET"]["LOGIN"]["profile name"]
        self.ui.cookieInput.setPlainText(cookie)
        self.ui.userInput.setText(username)
        self.ui.passInput.setText(password)
        self.ui.twoFAInput.setText(twoFA)
        self.ui.profileName.setText(profile_name)
        if self.ui.fullLoginCheckBox.isChecked():
            if settings.using2FA:
                self.ui.fullLoginInput.setText(username+"|"+password+"|"+twoFA)
            else:
                self.ui.fullLoginInput.setText(username+"|"+password)
    
    def save_data(self):
        if self.ui.getStacked.currentWidget() == self.ui.loginPage:
            if self.ui.fullLoginCheckBox.isChecked():
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
        self.data_manager.data["GET"]["LOGIN"]["username"] = username
        self.data_manager.data["GET"]["LOGIN"]["password"] = password
        self.data_manager.data["GET"]["LOGIN"]["2fa"] = twoFA
        self.data_manager.data["GET"]["LOGIN"]["cookie"] = cookie
        if self.ui.profileName.text() != "":
            self.data_manager.data["GET"]["LOGIN"]["profile name"] = self.ui.profileName.text()