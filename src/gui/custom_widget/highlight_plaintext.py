from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPalette, QColor

class HighlightPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_palette = self.palette()
        self.highlight_palette = QPalette()
        self.highlight_palette.setColor(QPalette.ColorRole.Text, QColor("yellow"))
        
    def setPlainText(self, text: str) -> None:
        super().setPlainText(text)
        if text:  # Only highlight if text is not empty
            self.setPalette(self.highlight_palette)
            QTimer.singleShot(1000, self.resetColor)
    
    def resetColor(self):
        self.setPalette(self.default_palette)