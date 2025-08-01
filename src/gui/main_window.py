from PySide6.QtWidgets import QMainWindow, QPushButton, QFileDialog, QFrame, QGraphicsDropShadowEffect, QTableWidgetItem
from PySide6.QtCore import QEvent, QPoint, Qt, QPropertyAnimation, QEasingCurve, QTimer, QRect, QThreadPool
from PySide6.QtGui import QShortcut, QKeySequence, QColor

from src.gui.window_control import WindowController
from src.gui.styles import MENU_SELECTED_STYLE, MENU_NONE_SECLECTED_STYLE

from src.gui.custom_widget.table_widget import TableWidget
from src.gui.styles import *
import src.settings as settings

from src.gui.widget import Ui_MainWindow, GetUI, PostUI, CommentUI, SpamUI
from src.worker import Post, Login, Spam, GetGroup, GetPost

from src.manager import DriverManager, DataManager

import pyperclip, os

DATA_FOLDER = "data"
CHROME_PATH = DATA_FOLDER + "/ChromeData"
DATA_PATH = DATA_FOLDER + "/Data.json"

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.window_controller = WindowController(self)

        # Minimize window
        self.ui.minimizeBtn.clicked.connect(self.showMinimized)
        # Close window
        self.ui.closeBtn.clicked.connect(self.close)
        # Restore/Maximize window
        self.ui.changeWindowBtn.clicked.connect(self.window_controller.maximize_restore)
        # Side bar
        self.ui.btn_toggle.clicked.connect(self.toggleMenu)
        
        self.data_manager = DataManager(DATA_FOLDER, DATA_PATH)
        self.data_manager.load_data()
        self.driver_manager = DriverManager(CHROME_PATH if ":" in CHROME_PATH else os.path.join(os.getcwd(), CHROME_PATH))
        
        self.post_ui = PostUI(self.ui, self.data_manager)
        self.comment_ui = CommentUI(self.ui, self.data_manager)
        self.spam_ui = SpamUI(self.ui, self.data_manager)
        self.get_ui = GetUI(self.ui, self.data_manager)
        self.table_widget = TableWidget(self)
        
        self.post = Post(self.driver_manager, self.data_manager)
        self.login = Login(self.driver_manager, self.data_manager)
        self.get_group = GetGroup(self.driver_manager, self.data_manager)
        self.get_post = GetPost(self.driver_manager, self.data_manager)
        self.spam = Spam(self.driver_manager, self.data_manager)
    
        # Connect signal update ui
        self.post.signals.log.connect(lambda msg: self.table_widget.statusTable.setText(msg))
        self.post.signals.table_status.connect(lambda row, msg: self.table_widget.table.setItem(row, 3, QTableWidgetItem(msg)))
        self.post.signals.finished.connect(lambda: self.table_widget.btn_run.setText("POST"))
        
        self.login.signals.log.connect(lambda msg: self.ui.statusGet.setText(msg))
        self.login.signals.cookie_output.connect(lambda cookie: self.ui.cookieOutputText.setPlainText(cookie))
        self.login.signals.profile_name.connect(lambda profile_name: self.ui.profileName.setText(profile_name))
        self.login.signals.hide_loginFrame.connect(self.ui.loginFrame.hide)
        
        self.get_group.signals.log.connect(lambda msg: self.table_widget.statusTable.setText(msg))
        self.get_group.signals.add_row.connect(lambda link, name: self.table_widget.add_row(link, name))
        
        self.spam.signals.log.connect(lambda msg: self.ui.statusHome.setText(msg))
        self.spam.signals.finished.connect(lambda: self.ui.btn_spam.setText("SPAM!"))
        
        self.load()
        self.defaultSetting()
        # Menu
        self.ui.btn_home.clicked.connect(self.chooseMenu)
        self.ui.btn_get.clicked.connect(self.chooseMenu)
        self.ui.btn_proxy.clicked.connect(self.chooseMenu)
        self.ui.btn_save.clicked.connect(self.save_all)
        self.ui.btn_table.clicked.connect(None)

        # HOME
        self.ui.functionComboBox.activated.connect(self.chooseFunction)
        self.ui.btn_homeReload.clicked.connect(self.load)
        
        self.ui.spamSpamListFilter.stateChanged.connect(lambda: self.ui.spamListFilter.hide() if self.ui.spamListFilter.isVisible() else self.ui.spamListFilter.show())
        # self.ui.btn_postImageFromFile.clicked.connect(lambda: LoadImage("POST"))
        # self.ui.btn_commentImageFromFile.clicked.connect(lambda: LoadImage("COMMENT"))
        # self.ui.btn_spamImageFromFile.clicked.connect(lambda: LoadImage("SPAM"))
        # toolFunction.data[5].imagesShown.connect(lambda: toolFunction.SaveContent(self, "POST"))
        # toolFunction.data[6].imagesShown.connect(lambda: toolFunction.SaveContent(self, "COMMENT"))
        # toolFunction.data[7].imagesShown.connect(lambda: toolFunction.SaveContent(self, "SPAM"))
        # self.ui.postDelayInput.returnPressed.connect(lambda: toolFunction.updateUpDelay(self))
        # self.ui.commentDelayInput.returnPressed.connect(lambda: toolFunction.updateUpDelay(self))
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save)
        
        self.table_widget.btn_run.clicked.connect(self.run_in_table)
        self.ui.btn_spam.clicked.connect(self.run_spam)

        # GET
        # self.ui.getComboBox.activated.connect(self.chooseGet)
        # self.ui.btn_getReload.clicked.connect(lambda: toolFunction.LoadGet(self.ui))
        # self.ui.cookiesDetailCheckBox.stateChanged.connect(self.changeLoginUserPassMethod)
        # self.ui.loginDetailCheckBox.stateChanged.connect(self.changeLoginUserPassMethod)
        # self.ui.cookie2FACheckBox.clicked.connect(self.changeUseOf2FA)
        # self.ui.twoFACheckBox.clicked.connect(self.changeUseOf2FA)
        self.ui.btn_getCookie.clicked.connect(self.login.get_cookies)
        # self.ui.methodComboBox.activated.connect(self.chooseLoginMethod)
        self.ui.copyButton.clicked.connect(self.copy_cookies)
        
        # self.ui.btn_getGroup.clicked.connect(lambda: toolFunction.OpenTable(self, TableWindow(), "GET GROUP"))
        
        self.ui.btn_post.clicked.connect(self.open_table)
        self.ui.btn_comment.clicked.connect(self.open_table)
        self.ui.btn_getGroup.clicked.connect(self.open_table)
        self.ui.btn_getPost.clicked.connect(self.open_table)

        self.ui.btn_login.clicked.connect(self.login.run)

        # PROXY
        self.ui.proxyCheckBox.clicked.connect(self.changeStatusProxy)
        self.ui.btn_proxy.clicked.connect(self.changeStatusProxy)
        self.ui.proxyInputMethodCheckBox.stateChanged.connect(self.changeProxyInputMethod)
        
        # self.table_widget.resize(self.width() - self.ui.leftMenu.width() // 2, self.height() - self.ui.contentTop.height() - self.ui.bottomBar.height())
        # self.table_widget.move(self.ui.leftMenu.width() // 4, self.ui.contentTop.height() - 10)
        self.table_widget.hide()
        self.table_widget.setGraphicsEffect(None)
        self.table_animation = QPropertyAnimation(self.table_widget, b"geometry")

        self.show()
    
    def run_in_table(self):
        if "POST" in self.table_widget.btn_run.text():
            self.run_post()
        if "COMMENT" in self.table_widget.btn_run.text():
            self.run_comment()
        if self.table_widget.btn_run.text() == "GET GROUP":
            self.run_getGroup()
        if self.table_widget.btn_run.text() == "GET POST":
            self.run_getPost()
        
    def run_post(self):
        if self.table_widget.btn_run.text() != "STOP POST!":
            self.table_widget.btn_run.setText("STOP POST!")
            if not self.driver_manager.setup_driver():
                self.table_widget.statusTable.setText("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
                return
            self.driver_manager.jump_to_facebook()
            if not self.driver_manager.is_login:
                self.table_widget.statusTable.setText("POST: Chưa đăng nhập")
                return
            self.move(self.screen().size().width()- self.size().width(), self.screen().size().height() - self.size().height() - 50)
            self.post_ui.save_data()
            
            self.post.setup(self.table_widget.get_selected(), self.ui.postContentCheckBox.isChecked(), self.ui.postImageCheckBox.isChecked())
            self.post.set_stop(False)  # Tell Spam to keep running
            QThreadPool.globalInstance().start(self.post)
        else:
            self.table_widget.statusTable.setText("POST: Đã tạm dừng")
            self.table_widget.btn_run.setText("POST")
            self.post.set_stop(True)
    
    def run_comment(self):
        return
    
    def run_getGroup(self):
        self.table_widget.table.setRowCount(0)
        filter_keys = [keyword.strip() for keyword in self.table_widget.filterGroupInput.text().split(",") if keyword.strip()]
        self.get_group.setup(self.table_widget.filterGroupCheckBox.isChecked(), filter_keys)
        
        self.get_ui.save_data()
        
        if not self.driver_manager.setup_driver():
            self.table_widget.statusTable.setText("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            return
        self.driver_manager.jump_to_facebook()
        if not self.driver_manager.is_login:
            self.table_widget.statusTable.setText("Get Group: Chưa đăng nhập")
            return
        
        QThreadPool.globalInstance().start(self.get_group)
    
    def run_getPost(self):
        return
    
    def run_login(self):
        self.move(self.screen().size().width()- self.size().width(), self.screen().size().height() - self.size().height() - 50)
        
        self.get_ui.save_data()

        QThreadPool.globalInstance().start(self.login)
    
    def run_spam(self):
        if self.ui.btn_spam.text() != "STOP!":
            self.data_manager.data["SPAM"]["image"] = [img for img in self.data_manager.data["SPAM"]["image"] if img]
            self.data_manager.data["SPAM"]["content"] = [content for content in self.data_manager.data["SPAM"]["content"] if content]
            if not (self.data_manager.data["SPAM"]["image"] or self.data_manager.data["SPAM"]["content"]):
                self.ui.btn_spam.setText("SPAM!")
                self.ui.statusHome.setText("SPAM: Thiếu thông tin để đi spam")
                return
            self.ui.btn_spam.setText("STOP!")
            if not self.driver_manager.setup_driver():
                self.ui.statusHome.setText("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
                return
            self.driver_manager.jump_to_facebook()
            if not self.driver_manager.is_login:
                self.ui.statusHome.setText("SPAM: Chưa đăng nhập")
                return
            self.move(self.screen().size().width()- self.size().width(), self.screen().size().height() - self.size().height() - 50)
            self.spam_ui.save_data()
            
            self.spam.set_stop(False)  # Tell Spam to keep running
            QThreadPool.globalInstance().start(self.spam)
        else:
            self.ui.statusHome.setText("SPAM: Đã tạm dừng")
            self.ui.btn_spam.setText("CONTINUE")
            self.spam.set_stop(True)  # Tell Spam to pause
        
    def mousePressEvent(self, event):
        self.window_controller.handle_mouse_press(event)
        
    def resizeEvent(self, event):
        # Update Size Grips
        self.window_controller.update_grips_geometry()
        self.center_table()
        
    def load(self):
        """Load initial settings and data"""
        self.post_ui.load_data()
        self.comment_ui.load_data()
        self.spam_ui.load_data()
        self.get_ui.load_data()
        
        # Load images if available
        self.post_ui.load_image(use_dialog=False)
        self.comment_ui.load_image(use_dialog=False)
        self.spam_ui.load_image(use_dialog=False)
    
    def save(self):
        """Save data based on current active page"""
        current_page = self.ui.pageStacked.currentWidget()
        
        if current_page == self.ui.homePage:
            # Save based on current function in home page
            current_function = self.ui.functionComboBox.currentText()
            if current_function == "POST":
                self.post_ui.save_data()
            elif current_function == "COMMENT":
                self.comment_ui.save_data()
            elif current_function == "SPAM":
                self.spam_ui.save_data()
        elif current_page == self.ui.getPage:
            # Save GET data
            self.get_ui.save_data()
        
        try:
            self.data_manager.save_data()
            self.ui.statusHome.setText(f"Đã lưu dữ liệu {current_function}")
            self.ui.statusGet.setText(f"Đã lưu dữ liệu {current_function}")
        except:
            self.ui.statusHome.setText("Không thể lưu dữ liệu vào file đang mở, vui lòng đóng file " + self.data_manager.data_path.split("\\")[-1])
            self.ui.statusGet.setText("Không thể lưu dữ liệu vào file đang mở, vui lòng đóng file " + self.data_manager.data_path.split("\\")[-1])
    
    def save_all(self):
        """Save all data regardless of current page"""
        self.post_ui.save_data()
        self.comment_ui.save_data()
        self.spam_ui.save_data()
        self.get_ui.save_data()
        
        try:
            self.data_manager.save_data()
            self.ui.statusHome.setText("Đã lưu toàn bộ dữ liệu tool vào file " + self.data_manager.data_path.split("\\")[-1])
        except:
            self.ui.statusHome.setText("Không thể lưu dữ liệu vào file đang mở, vui lòng đóng file " + self.data_manager.data_path.split("\\")[-1])
        
    def defaultSetting(self):
        # toolFunction.LoadHome(self, first=True)
        # toolFunction.LoadGet(self)
        
        self.ui.pageStacked.setCurrentWidget(self.ui.homePage)
        self.ui.btn_home.setStyleSheet(MENU_SELECTED_STYLE)
        self.ui.commentImageCheckBox.setCheckState(Qt.CheckState.Unchecked)
        self.ui.commentImageViewer.hide()
        self.ui.btn_commentImageFromFile.hide()
        self.ui.spamImageCheckBox.setCheckState(Qt.CheckState.Unchecked)
        self.ui.spamImageViewer.hide()
        self.ui.btn_spamImageFromFile.hide()
        self.ui.functionComboBox.setCurrentText("POST")
        self.ui.homeStackedWidget.setCurrentWidget(self.ui.postPage)
        self.ui.getStacked.setCurrentWidget(self.ui.getGroupPostPage)
        self.ui.loginFrame.hide()
        self.ui.methodComboBox.setCurrentText("Cookie")
        self.ui.cookieLoginDetailFrame.hide()
        self.ui.loginDetailFrame.hide()
        self.ui.loginMethodStacked.setCurrentWidget(self.ui.useCookie)
        self.ui.proxyInputDetailFrame.hide()

    def open_table(self):
        """Animate expanding TableWidget from center"""
        if not self.table_widget.isVisible():
            self.center_table()  # Position it first
            self.table_widget.show()
            self.table_widget.setGeometry(QRect(self.table_widget.x() + self.table_frame_width // 2, self.table_widget.y() + self.table_frame_height // 2, 0, 0))

            self.table_animation.setStartValue(self.table_widget.geometry())  # Start from tiny size
            self.table_animation.setEndValue(QRect(self.ui.leftMenu.width() // 4, self.ui.contentTop.height() - 10, self.table_frame_width, self.table_frame_height))  # Expand fully
            self.table_animation.start()
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(100)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 150))
            self.table_animation.finished.connect(lambda: self.table_widget.setGraphicsEffect(self.shadow))
        sender = self.sender()
        if sender == self.ui.btn_post:
            self.table_widget.setup("POST")
        elif sender == self.ui.btn_comment:
            self.table_widget.setup("COMMENT")
        elif sender == self.ui.btn_getGroup:
            self.table_widget.setup("GET GROUP")
        elif sender == self.ui.btn_getPost:
            self.table_widget.setup("GET POST")
        
    def center_table(self):
        self.table_frame_width = self.width() - self.ui.leftMenu.width() // 2
        self.table_frame_height = self.height() - self.ui.contentTop.height() - self.ui.bottomBar.height()
        # self.table_widget.resize(self.table_frame_width, self.table_frame_height)
        # self.table_widget.move(self.ui.leftMenu.width() // 4, self.ui.contentTop.height() - 10)
        self.table_widget.setGeometry(QRect(self.ui.leftMenu.width() // 4, self.ui.contentTop.height() - 10, self.table_frame_width, self.table_frame_height))

    def toggleMenu(self):
        if self.ui.leftMenu.width() == settings.SIDE_MENU_WIDTH:
            width, widthExtend = settings.SIDE_MENU_WIDTH, settings.SIDE_MENU_EXTEND
        else:
            width, widthExtend = settings.SIDE_MENU_EXTEND, settings.SIDE_MENU_WIDTH
        self.animation = QPropertyAnimation(self.ui.leftMenu, b"minimumWidth")
        self.animation.setDuration(settings.TIME_ANIMATION)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtend)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
    def resetStyle(self, widget):
        for w in self.ui.leftMenuBtn.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(MENU_NONE_SECLECTED_STYLE)

    def chooseMenu(self):
        btn = self.sender()
        btnName = btn.objectName()
        self.resetStyle(btnName)
        btn.setStyleSheet(MENU_SELECTED_STYLE)
        if btnName == "btn_home":
            self.ui.pageStacked.setCurrentWidget(self.ui.homePage)
        if btnName == "btn_get":
            self.ui.pageStacked.setCurrentWidget(self.ui.getPage)
        if btnName == "btn_proxy":
            self.ui.pageStacked.setCurrentWidget(self.ui.proxyPage)
    
    def chooseFunction(self):
        currentFunc = self.ui.functionComboBox.currentText()
        if currentFunc == "POST":
            self.ui.homeStackedWidget.setCurrentWidget(self.ui.postPage)
        elif currentFunc == "COMMENT":
            self.ui.homeStackedWidget.setCurrentWidget(self.ui.commentPage)
        elif currentFunc == "SPAM":
            self.ui.homeStackedWidget.setCurrentWidget(self.ui.spamPage)
            
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
        '''%self.ui.cookieOutputText.toPlainText()
        pyperclip.copy(consoleCode)
        self.ui.statusGet.setText("Đã copy code cookies, paste vào console của chromeDevtool để login")
    
    # GET
    # def chooseGet(self):
    #     currentGet = self.ui.getComboBox.currentText()
    #     if currentGet == "GET COOKIE":
    #         self.ui.getStacked.setCurrentWidget(self.ui.getCookiePage)
    #     else:
    #         if self.ui.cookieInput != "":
    #             self.ui.loginFrame.hide()
    #         else:
    #             self.ui.loginFrame.show()
    #         self.ui.getStacked.setCurrentWidget(self.ui.getGroupPostPage)
    # def chooseLoginMethod(self):
    #     currentLoginMethod = self.ui.methodComboBox.currentText()
    #     if currentLoginMethod == "Username|Password|2fa":
    #         self.ui.loginMethodStacked.setCurrentWidget(self.ui.useUserPass)
    #     if currentLoginMethod == "Cookie":
    #         self.ui.loginMethodStacked.setCurrentWidget(self.ui.useCookie)
    def changeUseOf2FA(self):
        global using2FA
        using2FA = not using2FA
        # if using2FA:
        #     self.ui.cookie2FAInput.show()
        #     self.ui.twoFAInput.show()
        #     self.ui.cookieLoginCheckBox.setText("USER|PASS|2FA")
        #     self.ui.loginCheckBox.setText("USER|PASS|2FA")
        #     self.ui.cookieLoginInput.setText(self.ui.cookieUserInput.text()+"|"+self.ui.cookiePassInput.text()+"|"+self.ui.cookie2FAInput.text().replace(" ", ""))
        #     self.ui.loginInput.setText(self.ui.userInput.text()+"|"+self.ui.passInput.text()+"|"+self.ui.cookie2FAInput.text().replace(" ", ""))
        #     self.ui.cookie2FACheckBox.setCheckState(Qt.CheckState.Checked)
        #     self.ui.twoFACheckBox.setCheckState(Qt.CheckState.Checked)
        # else:
        #     self.ui.cookie2FAInput.hide()
        #     self.ui.twoFAInput.hide()
        #     self.ui.cookieLoginCheckBox.setText("USER|PASS")
        #     self.ui.loginCheckBox.setText("USER|PASS")
        #     self.ui.cookieLoginInput.setText(self.ui.cookieUserInput.text()+"|"+self.ui.cookiePassInput.text())
        #     self.ui.loginInput.setText(self.ui.userInput.text()+"|"+self.ui.passInput.text())
        #     self.ui.cookie2FACheckBox.setCheckState(Qt.CheckState.Unchecked)
        #     self.ui.twoFACheckBox.setCheckState(Qt.CheckState.Unchecked)
    def changeLoginUserPassMethod(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.cookieLoginInput.show()
            self.ui.cookieLoginDetailFrame.hide()
            self.ui.loginInput.show()
            self.ui.loginDetailFrame.hide()
            if using2FA:
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
            self.ui.loginDetailFrame.show()
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

    # PROXY
    def changeStatusProxy(self):
        if self.ui.btn_proxy.isChecked():
            self.ui.proxyCheckBox.setCheckState(Qt.CheckState.Checked)
            self.ui.proxyFrame.show()
        else:
            self.ui.proxyCheckBox.setCheckState(Qt.CheckState.Unchecked)
            self.ui.proxyFrame.hide()

    def changeProxyInputMethod(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.proxyInputDetailFrame.hide()
            self.ui.proxyInput.show()
        else:
            self.ui.proxyInputDetailFrame.show()
            self.ui.proxyInput.hide()