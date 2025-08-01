from PySide6.QtWidgets import QMainWindow, QSizeGrip, QPushButton, QTableWidgetItem, QFileDialog, QFrame, QGraphicsDropShadowEffect
from PySide6.QtCore import QEvent, QPoint, Qt, QPropertyAnimation, QEasingCurve, QTimer, QRect
from PySide6.QtGui import QShortcut, QKeySequence, QColor

from src.gui.widget.ui_tableWidget import Ui_tableWidget
from src.settings import TIME_ANIMATION

class TableWidget(QFrame, Ui_tableWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        
        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(100)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.setGraphicsEffect(self.shadow)
        
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(TIME_ANIMATION)  # Duration in milliseconds
        
        self.closeBtn.clicked.connect(self.animated_close)
        
    def animated_close(self):
        """Animate widget shrinking and then close"""
        self.animation.setStartValue(self.geometry())  # Start at current size

        # Shrink towards the center
        center_x = self.x() + self.width() // 2
        center_y = self.y() + self.height() // 2
        self.animation.setEndValue(QRect(center_x, center_y, 0, 0))
        # animation.setEasingCurve(QEasingCurve.InOutQuart)

        self.setGraphicsEffect(None)
        self.animation.start()
        self.animation.finished.connect(self.hide)  # Hide after animation ends
    
    def setup(self, func: str):
        match func:
            case "POST":
                self.btn_run.setText("POST")
                self.fromToFrame.show()
                self.latestPost.hide()
                self.filterGroup.hide()
                self.fromLabel.setText("Từ group")
                self.toLabel.setText("đến group")
                self.listLabel.setText("List group")
            case "COMMENT":
                self.fromToFrame.show()
                self.latestPost.hide()
                self.filterGroup.hide()
                self.fromLabel.setText("Từ post")
                self.toLabel.setText("đến post")
                self.listLabel.setText("ListPost")
            case "GET GROUP":
                self.btn_run.setText("GET GROUP")
                self.fromToFrame.hide()
                self.latestPost.hide()
                self.filterGroup.show()
            case "GET POST":
                self.btn_run.setText("GET POST")
                self.fromToFrame.show()
                self.latestPost.show()
                self.filterGroup.hide()
                self.fromLabel.setText("Từ group")
                self.toLabel.setText("đến group")
                self.listLabel.setText("List group")

    def get_selected(self):
        selected_rows = set(item.row() for item in self.table.selectedItems())
        if not selected_rows: return []
        if (self.btn_run.text() in ["POST", "STOP POST!", "GET POST"]):
            col = 0 # Group
        else: col = 1 # Post
        self.table.clearSelection()
        selected_items = []
        # Chọn lại các ô
        for row in selected_rows:
            self.table.item(row, col).setSelected(True)
            selected_items.append({
                "row": row,
                "link": self.table.item(row, col).text().strip(),
                "name group": self.table.item(row, 2).text().lower()
            })
        return selected_items
    
    def add_row(self, link: str, name: str):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(link))
        self.table.setItem(row_position, 2, QTableWidgetItem(name))