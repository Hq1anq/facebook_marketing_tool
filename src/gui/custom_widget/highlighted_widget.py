from PySide6.QtWidgets import QLabel, QPlainTextEdit
from PySide6.QtCore import QTimer

class HighlightLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_palette = self.palette()
        self.default_style = self.styleSheet()
        self.highlight_style = "color: yellow;"  # Apply text color
        
    def setText(self, text: str) -> None:
        super().setText(text)
        if text:  # Only highlight if text is not empty
            self.setStyleSheet(self.highlight_style)
            QTimer.singleShot(1000, self.resetColor)
    
    def resetColor(self):
        self.setStyleSheet(self.default_style)

class HighlightPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_palette = self.palette()
        self.default_style = self.styleSheet()
        self.highlight_style = "color: yellow;"  # Apply text color
        
    def setPlainText(self, text: str) -> None:
        super().setPlainText(text)
        if text:  # Only highlight if text is not empty
            self.setStyleSheet(self.highlight_style)
            QTimer.singleShot(1000, self.resetColor)
    
    def resetColor(self):
        self.setStyleSheet(self.default_style)