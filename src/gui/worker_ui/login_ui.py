from PySide6.QtCore import QThreadPool, Qt, QSize

import src.settings as settings
from src.manager import DataManager, DriverManager
from src.gui.widget.ui_interface import Ui_MainWindow
from src.worker import Login
from src.gui.styles import BUTTON_STYLE
import pyperclip

class LoginUI:
    def __init__(self, before_run, ui: Ui_MainWindow, data_manager: DataManager, driver_manager: DriverManager):
        self.ui = ui
        self.before_run = before_run
        self.data_manager = data_manager
        self.driver_manager = driver_manager

        self.worker = Login(driver_manager)
        self.worker.setAutoDelete(False)
        
        self.setup_connections()

    def setup_connections(self):
        self.worker.signals.loading.connect(self.ui.status.setLoading)
        self.worker.signals.error.connect(self.ui.status.setError)
        self.worker.signals.cookie_output.connect(lambda cookie: self.ui.cookieInput.setPlainText(cookie))
        self.worker.signals.finished.connect(self.on_login_success)
        
        self.ui.btn_reload_loginMethod.clicked.connect(self.load_data)
        self.ui.btn_login.clicked.connect(self.run_login)
        self.ui.btn_copyCookie.clicked.connect(self.copy_cookies)

        self.ui.methodComboBox.activated.connect(self.toggle_login_method)
        self.ui.loginDetail.stateChanged.connect(self.toggle_login_detail)
        self.ui.twoFACheckBox.stateChanged.connect(self.toggle_use_2fa)
    
    def on_login_success(self, profile_name):
        self.ui.status.setSuccess("Đăng nhập thành công, profile: " + profile_name)
        self.updateProfileName(profile_name)
    
    def updateProfileName(self, name):
        if (name):
            self.ui.profileName.setText(name)
            self.ui.profileName.setIconSize(QSize(40, 40))
            self.ui.profileName.setStyleSheet(None)
        else:
            self.ui.profileName.setText("LOGIN")
            self.ui.profileName.setIconSize(QSize(0, 0))
            self.ui.profileName.setStyleSheet(BUTTON_STYLE)
    
    def run_login(self):
        try:
            self.save_data()
        except SyntaxError as e:
            self.ui.status.setError(str(e))
            return
        cookie = self.data_manager.data["ACCOUNT"]["LOGIN"]["cookie"]
        username = self.data_manager.data["ACCOUNT"]["LOGIN"]["username"]
        password = self.data_manager.data["ACCOUNT"]["LOGIN"]["password"]
        twofa = self.data_manager.data["ACCOUNT"]["LOGIN"]["2fa"]

        type_login = "cookie" if self.ui.loginMethodStacked.currentWidget() == self.ui.useCookie else "username"
        if type_login == "cookie" and cookie == "":
            self.ui.status.setError("Thiếu cookie")
            return
        elif type_login == "username" and (not (username and password)):
            self.ui.status.setError("Thiếu thông tin đăng nhập")
            return

        self.before_run()
        self.ui.status.setLoading("Đang đăng nhập...")
        self.worker.setup(cookie, username, password, twofa, type_login)
        QThreadPool.globalInstance().start(self.worker)
    
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
        cookie = self.data_manager.data["ACCOUNT"]["LOGIN"]["cookie"]
        username = self.data_manager.data["ACCOUNT"]["LOGIN"]["username"]
        password = self.data_manager.data["ACCOUNT"]["LOGIN"]["password"]
        twoFA = self.data_manager.data["ACCOUNT"]["LOGIN"]["2fa"]
        profile_name = self.data_manager.data["ACCOUNT"]["LOGIN"]["profile name"]
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
        username, password, twoFA = "", "", ""
        if self.ui.loginDetail.isChecked():
            username = self.ui.userInput.text()
            password = self.ui.passInput.text()
            twoFA = self.ui.twoFAInput.text()
        else:
            info = self.ui.fullLoginInput.text().split("|")
            if len(info) >= 2:
                username = info[0]
                password = info[1]
            if len(info) == 3:
                twoFA = info[2].replace(" ", "")
            if len(info) < 2:
                raise SyntaxError("Sai định dạng dữ liệu login")
        cookie = self.ui.cookieInput.toPlainText()
        self.data_manager.data["ACCOUNT"]["LOGIN"]["username"] = username
        self.data_manager.data["ACCOUNT"]["LOGIN"]["password"] = password
        self.data_manager.data["ACCOUNT"]["LOGIN"]["2fa"] = twoFA
        self.data_manager.data["ACCOUNT"]["LOGIN"]["cookie"] = cookie
        if self.ui.profileName.text() != "LOGIN":
            self.data_manager.data["ACCOUNT"]["LOGIN"]["profile name"] = self.ui.profileName.text()
    
    def copy_cookies(self):
        consoleCode = '''
        void (function () {
            function setCookie(t) {
                var list = t.split("; ");
                console.log(list);
                for (var i = list.length - 1; i >= 0; i--) {
                    var cname = list[i].split("=")[0];
                    var cvalue = list[i].split("=")[1];
                    document.cookie = cname + "=" + cvalue;
                }
            }
            setCookie("%s");
            location.href = "https://facebook.com";
        })();
        '''%self.ui.cookieInput.toPlainText()
        pyperclip.copy(consoleCode)
        self.ui.status.setSuccess("Đã copy code cookies, paste vào console của chromeDevtool để login")