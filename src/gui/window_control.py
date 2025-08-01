from PySide6.QtWidgets import QMainWindow, QSizeGrip
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QMouseEvent
from src.gui.custom_widget.custom_grips import CustomGrip
from src.gui.widget.ui_interface import Ui_MainWindow

class WindowController:
    def __init__(self, window: QMainWindow):
        self.window = window
        self.ui: Ui_MainWindow = window.ui
        self.dragPos = None
        self._normal_geometry = None  # Save normal geometry before maximize
        
        # Remove window tittle bar
        self.window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Setup window controls
        self.setup_title_bar()
        self.setup_size_grips()
        
    def setup_title_bar(self):
        """Setup title bar double click and drag events"""
        def doubleClickMaximizeRestore(event: QMouseEvent):
            if event.type() == QEvent.Type.MouseButtonDblClick:
                self.ui.changeWindowBtn.click()
                
        def moveWindow(event: QMouseEvent):
            if self.ui.changeWindowBtn.isChecked(): # Window is maximize
                
                # Calculate offset from mouse to window's top-left in normal geometry
                mouse_global = event.globalPosition().toPoint()
                maximize_geometry = self.window.geometry()
                
                # Restore window to normal
                self.ui.changeWindowBtn.setChecked(False)
                self.maximize_restore(False)
                
                # Center the cursor on the window when dragging from maximized state
                # self.window.move(event.globalPosition().toPoint() - QPoint(self.window.width()/2, 0))
                
                # Move window so mouse stays at the same relative position
                x_ratio = (mouse_global.x() - maximize_geometry.x()) / maximize_geometry.width()
                y_ratio = (mouse_global.y() - maximize_geometry.y()) / maximize_geometry.height()
                # Move window so that mouse is at the same relative position on restored window
                new_x = mouse_global.x() - x_ratio * self._normal_geometry.width()
                new_y = mouse_global.y() - y_ratio * self._normal_geometry.height()
                self.window.move(new_x, new_y)
                # Update dragPos for smooth dragging
                self.dragPos = mouse_global
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.window.move(self.window.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()
                
        self.ui.contentTop.mouseDoubleClickEvent = doubleClickMaximizeRestore
        self.ui.title.mouseMoveEvent = moveWindow
        
    def setup_size_grips(self):
        """Setup window resize grips"""
        self.sizegrip = QSizeGrip(self.ui.sizeGrip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")
        
        # Custom grips for each edge
        self.left_grip = CustomGrip(self.window, Qt.Edge.LeftEdge, True)
        self.right_grip = CustomGrip(self.window, Qt.Edge.RightEdge, True)
        self.top_grip = CustomGrip(self.window, Qt.Edge.TopEdge, True)
        self.bottom_grip = CustomGrip(self.window, Qt.Edge.BottomEdge, True)
        
        self.update_grips_geometry()
        
    def update_grips_geometry(self):
        """Update size grips position and size"""
        self.left_grip.setGeometry(0, 5, 5, self.window.height())
        self.right_grip.setGeometry(self.window.width() - 5, 5, 5, self.window.height())
        self.top_grip.setGeometry(0, 0, self.window.width(), 5)
        self.bottom_grip.setGeometry(0, self.window.height() - 5, self.window.width(), 5)
        
    def maximize_restore(self, checked):
        """Toggle between maximized and normal window state"""
        if not checked:
            self.window.showNormal()
            self.ui.sizeGrip.show()
            self._show_grips()
        else:
            self._normal_geometry = self.window.geometry()
            self.window.showMaximized()
            self.ui.sizeGrip.hide()
            self._hide_grips()
            
    def _show_grips(self):
        """Show all resize grips"""
        self.left_grip.show()
        self.right_grip.show()
        self.top_grip.show()
        self.bottom_grip.show()
        
    def _hide_grips(self):
        """Hide all resize grips"""
        self.left_grip.hide()
        self.right_grip.hide()
        self.top_grip.hide()
        self.bottom_grip.hide()
        
    def handle_mouse_press(self, event: QMouseEvent):
        """Handle mouse press for window dragging"""
        self.dragPos = event.globalPosition().toPoint()