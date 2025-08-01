from PySide6.QtCore import Qt

import src.settings as settings
from src.manager import DataManager
from src.gui.widget.ui_interface import Ui_MainWindow

class GetUI:
    def __init__(self, ui: Ui_MainWindow, data_manager: DataManager):
        self.ui = ui
        self.data_manager = data_manager

    def setup_connections(self):
        self.ui.getComboBox.activated.connect(self.toggle_get_type)
        self.ui.btn_getReload.clicked.connect(self.load_data)
        
        # Login Page
        self.ui.methodComboBox.activated.connect(self.toggle_login_method)
        self.ui.loginCheckBox.stateChanged.connect(self.toggle_login_detail)
        self.ui.twoFACheckBox.stateChanged.connect(self.toggle_use_2fa)
        
        # Cookie Page
        self.ui.cookieLoginCheckBox.stateChanged.connect(self.toggle_login_detail)
        self.ui.cookie2FACheckBox.clicked.connect(self.toggle_use_2fa)
    
    def toggle_get_type(self):
        if self.ui.getComboBox.currentText() == "GET COOKIE":
            self.ui.getStacked.setCurrentWidget(self.ui.getCookiePage)
        else:
            if self.ui.cookieInput != "":
                self.ui.loginFrame.hide()
            else:
                self.ui.loginFrame.show()
            self.ui.getStacked.setCurrentWidget(self.ui.getGroupPostPage)
    
    def toggle_login_method(self):
        if self.ui.methodComboBox.currentText() == "Username|Password|2fa":
            self.ui.loginMethodStacked.setCurrentWidget(self.ui.useUserPass)
        else:
            self.ui.loginMethodStacked.setCurrentWidget(self.ui.useCookie)
    
    def toggle_login_detail(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.cookieLoginInput.show()
            self.ui.cookieLoginDetailFrame.hide()
            self.ui.loginInput.show()
            self.ui.loginFrame.hide()
            if self.ui.twoFACheckBox.checkState() == Qt.CheckState.Checked:
                infoCookie = self.ui.cookieUserInput.text()+"|"+self.ui.cookiePassInput.text()+"|"+self.ui.cookie2FAInput.text()
                infoGroup = self.ui.userInput.text()+"|"+self.ui.passInput.text()+"|"+self.ui.twoFAInput.text()
            else:
                infoCookie = self.ui.cookieUserInput.text()+"|"+self.ui.cookiePassInput.text()
                infoGroup = self.ui.userInput.text()+"|"+self.ui.passInput.text()
            self.ui.cookieLoginInput.setText(infoCookie)
            self.ui.loginInput.setText(infoGroup)
        else:
            self.ui.cookieLoginInput.hide()
            self.ui.cookieLoginDetailFrame.show()
            self.ui.loginInput.hide()
            self.ui.loginFrame.show()
            infoCookie = self.ui.cookieLoginInput.text().split("|")
            infoGroup = self.ui.loginInput.text().split("|")
            if len(infoCookie) >= 2:
                self.ui.cookieUserInput.setText(infoCookie[0])
                self.ui.cookiePassInput.setText(infoCookie[1])
            if len(infoCookie) == 3:
                self.ui.cookie2FAInput.setText(infoCookie[2].replace(" ", ""))
            if len(infoGroup) >= 2:
                self.ui.userInput.setText(infoGroup[0])
                self.ui.passInput.setText(infoGroup[1])
            if len(infoGroup) == 3:
                self.ui.twoFAInput.setText(infoGroup[2].replace(" ", ""))
    
    def toggle_use_2fa(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.cookie2FAInput.show()
            self.ui.twoFAInput.show()
            self.ui.cookieLoginCheckBox.setText("USER|PASS|2FA")
            self.ui.loginCheckBox.setText("USER|PASS|2FA")
            self.ui.cookieLoginInput.setText(self.ui.cookieUserInput.text()+"|"+self.ui.cookiePassInput.text()+"|"+self.ui.cookie2FAInput.text().replace(" ", ""))
            self.ui.loginInput.setText(self.ui.userInput.text()+"|"+self.ui.passInput.text()+"|"+self.ui.cookie2FAInput.text().replace(" ", ""))
            self.ui.cookie2FACheckBox.setCheckState(Qt.CheckState.Checked)
            self.ui.twoFACheckBox.setCheckState(Qt.CheckState.Checked)
        else:
            self.ui.cookie2FAInput.hide()
            self.ui.twoFAInput.hide()
            self.ui.cookieLoginCheckBox.setText("USER|PASS")
            self.ui.loginCheckBox.setText("USER|PASS")
            self.ui.cookieLoginInput.setText(self.ui.cookieUserInput.text()+"|"+self.ui.cookiePassInput.text())
            self.ui.loginInput.setText(self.ui.userInput.text()+"|"+self.ui.passInput.text())
            self.ui.cookie2FACheckBox.setCheckState(Qt.CheckState.Unchecked)
            self.ui.twoFACheckBox.setCheckState(Qt.CheckState.Unchecked)

    def load_data(self):
        cookie = self.data_manager.data["GET"]["LOGIN"]["cookie"]
        username = self.data_manager.data["GET"]["LOGIN"]["username"]
        password = self.data_manager.data["GET"]["LOGIN"]["password"]
        twoFA = self.data_manager.data["GET"]["LOGIN"]["2fa"]
        profile_name = self.data_manager.data["GET"]["LOGIN"]["profile name"]
        self.ui.cookieOutputText.setPlainText(cookie)
        self.ui.cookieInput.setPlainText(cookie)
        self.ui.cookieUserInput.setText(username)
        self.ui.userInput.setText(username)
        self.ui.cookiePassInput.setText(password)
        self.ui.passInput.setText(password)
        self.ui.cookie2FAInput.setText(twoFA)
        self.ui.twoFAInput.setText(twoFA)
        self.ui.profileName.setText(profile_name)
        if self.ui.cookieLoginCheckBox.checkState() == Qt.CheckState.Checked:
            if settings.using2FA:
                self.ui.cookieLoginInput.setText(username+"|"+password+"|"+twoFA)
            else:
                self.ui.cookieLoginInput.setText(username+"|"+password)
        if self.ui.loginCheckBox.checkState() == Qt.CheckState.Checked:
            if settings.using2FA:
                self.ui.loginInput.setText(username+"|"+password+"|"+twoFA)
            else:
                self.ui.loginInput.setText(username+"|"+password)
    
    def save_data(self):
        if self.ui.getStacked.currentWidget() == self.ui.getCookiePage:
            if self.ui.cookieLoginCheckBox.checkState() == Qt.CheckState.Checked:
                info = self.ui.cookieLoginInput.text().split("|")
                if len(info) >= 2:
                    username = info[0]
                    password = info[1]
                if len(info) == 3:
                    twoFA = info[2].replace(" ", "")
            else:
                username = self.ui.cookieUserInput.text()
                password = self.ui.cookiePassInput.text()
                twoFA = self.ui.cookie2FAInput.text()
        elif self.ui.getStacked.currentWidget() == self.ui.getGroupPostPage:
            if self.ui.loginCheckBox.checkState() == Qt.CheckState.Checked:
                info = self.ui.loginInput.text().split("|")
                if len(info) >= 2:
                    username = info[0]
                    password = info[1]
                if len(info) == 3:
                    twoFA = info[2].replace(" ", "")
            else:
                username = self.ui.userInput.text()
                password = self.ui.passInput.text()
                twoFA = self.ui.twoFAInput.text().replace(" ", "")
            if self.ui.cookieOutputText.toPlainText() != "":
                cookie = self.ui.cookieOutputText.toPlainText()
            else:
                cookie = self.ui.cookieInput.toPlainText()
        self.data_manager.data["GET"]["LOGIN"]["username"] = username
        self.data_manager.data["GET"]["LOGIN"]["password"] = password
        self.data_manager.data["GET"]["LOGIN"]["2fa"] = twoFA
        self.data_manager.data["GET"]["LOGIN"]["cookie"] = cookie
        if self.ui.profileName.text() != "":
            self.data_manager.data["GET"]["LOGIN"]["profile name"] = self.ui.profileName.text()