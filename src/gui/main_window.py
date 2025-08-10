from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QThreadPool
from PySide6.QtGui import QShortcut, QKeySequence

from src.gui.styles import MENU_SELECTED_STYLE, MENU_NONE_SECLECTED_STYLE

from src.gui.custom_widget.table_widget import TableWidget
from src.gui.styles import *
import src.settings as settings

from .widget.ui_interface import Ui_MainWindow
from .window_control import WindowController
from src.gui.worker_ui import GetUI, PostUI, CommentUI, SpamUI
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
        
        self.post.setAutoDelete(False)
        self.spam.setAutoDelete(False)
    
        # Connect signal update ui
        self.post.signals.log.connect(lambda msg: self.table_widget.statusTable.setText(msg))
        self.post.signals.table_status.connect(lambda row, status: self.table_widget.table.setCellWidget(row, 3, self.table_widget.status_chip(status)))
        self.post.signals.finished.connect(lambda: self._on_finished_use_table("POST"))
        
        self.login.signals.log.connect(lambda msg: self.ui.statusGet.setText(msg))
        self.login.signals.cookie_output.connect(lambda cookie: self.ui.cookieInput.setPlainText(cookie))
        self.login.signals.profile_name.connect(lambda profile_name: self.ui.profileName.setText(profile_name))
        
        self.get_group.signals.log.connect(lambda msg: self.table_widget.statusTable.setText(msg))
        self.get_group.signals.add_row.connect(lambda link, name: self.table_widget.add_row(link, name))
        self.get_group.signals.finished.connect(self.table_widget.adjust_column_width)
        
        self.spam.signals.log.connect(lambda msg: self.ui.statusHome.setText(msg))
        self.spam.signals.finished.connect(lambda: self.ui.btn_spam.setText("SPAM!"))
        
        self.load()
        self.defaultSetting()
        # Menu
        self.ui.btn_home.clicked.connect(self.chooseMenu)
        self.ui.btn_get.clicked.connect(self.chooseMenu)
        self.ui.btn_proxy.clicked.connect(self.chooseMenu)
        self.ui.btn_save.clicked.connect(self.save_all)

        # HOME
        self.ui.functionComboBox.activated.connect(self.chooseFunction)
        self.ui.btn_homeReload.clicked.connect(self.load)
        
        self.ui.spamSpamListFilter.stateChanged.connect(lambda: self.ui.spamListFilter.hide() if self.ui.spamListFilter.isVisible() else self.ui.spamListFilter.show())
        # self.ui.btn_commentImageFromFile.clicked.connect(lambda: LoadImage("COMMENT"))
        # self.ui.btn_spamImageFromFile.clicked.connect(lambda: LoadImage("SPAM"))
        # toolFunction.data[5].imagesShown.connect(lambda: toolFunction.SaveContent(self, "POST"))
        # toolFunction.data[6].imagesShown.connect(lambda: toolFunction.SaveContent(self, "COMMENT"))
        # toolFunction.data[7].imagesShown.connect(lambda: toolFunction.SaveContent(self, "SPAM"))
        # self.ui.postDelayInput.returnPressed.connect(lambda: toolFunction.updateUpDelay(self))
        # self.ui.commentDelayInput.returnPressed.connect(lambda: toolFunction.updateUpDelay(self))
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        save_shortcut.activated.connect(self.save)
        
        self.table_widget.btn_run.clicked.connect(self.run_in_table)
        self.table_widget.tableExport.clicked.connect(self.save_in_table)
        self.ui.btn_spam.clicked.connect(self.run_spam)

        # GET
        # self.ui.btn_getReload.clicked.connect(lambda: toolFunction.LoadGet(self.ui))
        # self.ui.loginDetailCheckBox.stateChanged.connect(self.changeLoginUserPassMethod)
        # self.ui.twoFACheckBox.clicked.connect(self.changeUseOf2FA)
        # self.ui.methodComboBox.activated.connect(self.chooseLoginMethod)
        self.ui.btn_copyCookie.clicked.connect(self.copy_cookies)
        
        self.ui.btn_post.clicked.connect(self.open_table)
        self.ui.btn_comment.clicked.connect(self.open_table)
        self.ui.btn_getGroup.clicked.connect(self.open_table)
        self.ui.btn_getPost.clicked.connect(self.open_table)

        self.ui.btn_login.clicked.connect(self.run_login)

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
    
    def open_table(self):
        if not self.table_widget.isVisible():
            self.center_table()  # Position it first
            self.table_widget.show()
        self.table_widget.load_group_table(self.data_manager.data)
        # self.table_widget.table.setSpan(2, 1, 2, 1)  # Start at (0,1), span 2 rows, 1 column
        # self.table_widget.table.setItem(2, 1, QTableWidgetItem("Merged"))
        sender = self.sender()
        if sender == self.ui.btn_post:
            self.post_ui.save_data()
            self.table_widget.setup("POST")
        elif sender == self.ui.btn_comment:
            self.table_widget.setup("COMMENT")
        elif sender == self.ui.btn_getGroup:
            self.table_widget.setup("GET GROUP")
        elif sender == self.ui.btn_getPost:
            self.table_widget.setup("GET POST")
        self.table_widget.adjust_column_width()
    
    def save_in_table(self):
        if self.table_widget.btn_run.text() == "GET GROUP" or "POST" in self.table_widget.btn_run.text():
            self.save_group_table()
            
    def _on_finished_use_table(self, func: str):
        self.table_widget.btn_run.setText(func)
        self.table_widget.adjust_column_width()
        self.save_in_table()
        
    def run_post(self):
        self.move(self.screen().size().width()- self.size().width(), self.screen().size().height() - self.size().height() - 50)
        if self.table_widget.btn_run.text() != "STOP POST!":
            self.post_ui.save_data()
            post_data = self.data_manager.data["POST"]
            if not (post_data["image"] or post_data["content"]):
                self.ui.statusHome.setText("SPAM: Thiếu thông tin để đi spam")
                return
            if not self.driver_manager.setup_driver():
                self.table_widget.statusTable.setText("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
                return
            self.driver_manager.jump_to_facebook()
            if not self.driver_manager.is_login:
                self.handle_unLogin()
                return
            self.ui.profileName.setText(self.driver_manager.get_username())
            
            self.table_widget.btn_run.setText("STOP POST!")
            self.post.setup(self.table_widget.get_selected(), self.ui.postContentCheckBox.isChecked(), self.ui.postImageCheckBox.isChecked())
            self.post.set_stop(False)  # Tell Spam to keep running
            QThreadPool.globalInstance().start(self.post)
        else:
            self.table_widget.statusTable.setText("POST: Đã tạm dừng")
            self.table_widget.btn_run.setText("POST")
            self.post.set_stop(True)
    
    def run_comment(self):
        self.move(self.screen().size().width() - self.size().width(), self.screen().size().height() - self.size().height() - 50)
    
    def run_getGroup(self):
        self.move(self.screen().size().width() - self.size().width(), self.screen().size().height() - self.size().height() - 50)
        filter_keys = [keyword.strip() for keyword in self.table_widget.filterGroupInput.text().split(",") if keyword.strip()]
        
        if not self.driver_manager.setup_driver():
            self.ui.statusGet.setText("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            return
        self.driver_manager.jump_to_facebook()
        if not self.driver_manager.is_login:
            self.handle_unLogin()
            return
        self.ui.profileName.setText(self.driver_manager.get_username())
        
        self.get_group.setup(self.table_widget.filterGroupCheckBox.isChecked(), filter_keys)
        
        self.get_ui.save_data()
        
        self.table_widget.table.setRowCount(1) # Clear table
        QThreadPool.globalInstance().start(self.get_group)
    
    def run_getPost(self):
        self.move(self.screen().size().width() - self.size().width(), self.screen().size().height() - self.size().height() - 50)
        
        if not self.driver_manager.setup_driver():
            self.ui.statusGet.setText("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            return
        self.driver_manager.jump_to_facebook()
        if not self.driver_manager.is_login:
            self.handle_unLogin()
            return
        self.ui.profileName.setText(self.driver_manager.get_username())
    
    def run_login(self):
        self.move(self.screen().size().width()- self.size().width(), self.screen().size().height() - self.size().height() - 50)
        
        self.get_ui.save_data()
        
        if not self.driver_manager.setup_driver():
            self.ui.statusHome.setText("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            return
        self.driver_manager.jump_to_facebook()
        if self.driver_manager.is_login:
            self.ui.profileName.setText(self.driver_manager.get_username())
            return
        QThreadPool.globalInstance().start(self.login)
    
    def run_spam(self):
        self.move(self.screen().size().width()- self.size().width(), self.screen().size().height() - self.size().height() - 50)
        if self.ui.btn_spam.text() != "STOP!":
            self.spam_ui.save_data()
            spam_data = self.data_manager.data["SPAM"]
            if not (spam_data["image"] or spam_data["content"]):
                self.ui.statusHome.setText("SPAM: Thiếu thông tin để đi spam")
                return
            if not self.driver_manager.setup_driver():
                self.ui.statusHome.setText("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
                return
            self.driver_manager.jump_to_facebook()
            if not self.driver_manager.is_login:
                self.handle_unLogin()
                return
            self.ui.profileName.setText(self.driver_manager.get_username())
            
            self.ui.btn_spam.setText("STOP!")
            self.spam.setup(self.ui.spamContentCheckBox.isChecked(), self.ui.spamImageCheckBox.isChecked(), self.ui.spamSpamListFilter.isChecked())
            self.spam.set_stop(False)  # Tell Spam to keep running
            QThreadPool.globalInstance().start(self.spam)
        else:
            self.ui.statusHome.setText("SPAM: Đã tạm dừng")
            self.ui.btn_spam.setText("CONTINUE")
            self.spam.set_stop(True)  # Tell Spam to pause
    
    def handle_unLogin(self):
        if self.table_widget.isVisible():
            self.table_widget.hide()
        self.ui.btn_get.click()
        self.ui.getComboBox.setCurrentIndex(1)
        self.ui.getStacked.setCurrentWidget(self.ui.loginPage)
        self.ui.statusGet.setText("Bạn chưa đăng nhập, vui lòng đăng nhập trước khi sử dụng chức năng này")
            
    def save_group_table(self):
        """Save current table content to data_manager.data['GET']['GROUP']"""
        group_list = []
        for row in range(1, self.table_widget.table.rowCount()): # except filter row
            link_group = self.table_widget.table.item(row, 0).text() if self.table_widget.table.item(row, 0) else ""
            link_post = self.table_widget.table.item(row, 1).text() if self.table_widget.table.item(row, 1) else ""
            name_group = self.table_widget.table.item(row, 2).text() if self.table_widget.table.item(row, 2) else ""
            
            # ✅ Get status from custom chip widget
            status_widget = self.table_widget.table.cellWidget(row, 3)
            if status_widget:
                label = status_widget.findChild(QLabel)
                status = label.text() if label else ""
            else:
                status = ""

            group_data = {
                "link group": link_group,
                "link post": link_post,
                "name group": name_group,
                "status": status
            }
            group_list.append(group_data)

        # Save to data manager
        self.data_manager.data["GET"]["GROUP"] = group_list
        success = self.data_manager.save_data()
        
        if success:
            self.table_widget.statusTable.setText("Đã lưu dữ liệu bảng vào " + self.data_manager.data_path)
        else:
            self.table_widget.statusTable.setText("Lỗi: không thể lưu dữ liệu")
        
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
            current_function = "LOGIN" if self.ui.getStacked.currentWidget() == self.ui.loginPage else "GET DATA"
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
        self.ui.getStacked.setCurrentWidget(self.ui.getDataPage)
        self.ui.methodComboBox.setCurrentText("Cookie")
        self.ui.loginDetailFrame.hide()
        self.ui.loginMethodStacked.setCurrentWidget(self.ui.useCookie)
        self.ui.proxyInputDetailFrame.hide()
        
    def center_table(self):
        self.table_frame_width = self.width()
        self.table_frame_height = self.height() - self.ui.contentTop.height() - self.ui.bottomBar.height() + 18
        self.table_widget.setGeometry(QRect(0, self.ui.contentTop.height() - 10 - 9, self.table_frame_width, self.table_frame_height))

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
        '''%self.ui.cookieInput.toPlainText()
        pyperclip.copy(consoleCode)
        self.ui.statusGet.setText("Đã copy code cookies, paste vào console của chromeDevtool để login")

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