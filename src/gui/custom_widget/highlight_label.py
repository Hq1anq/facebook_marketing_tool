from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPalette, QColor

class HighlightLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_palette = self.palette()
        self.highlight_palette = QPalette()
        self.highlight_palette.setColor(QPalette.ColorRole.WindowText, QColor("yellow"))
        
    def setText(self, text: str) -> None:
        super().setText(text)
        if text:  # Only highlight if text is not empty
            self.setPalette(self.highlight_palette)
            QTimer.singleShot(1000, self.resetColor)
    
    def resetColor(self):
        self.setPalette(self.default_palette)