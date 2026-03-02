from PySide6.QtWidgets import QLabel, QPlainTextEdit
from PySide6.QtCore import QTimer

class HighlightLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_palette = self.palette()
        self.default_style = self.styleSheet()
        self.highlight_style = "color: yellow"
        self.success_style = "color: rgb(40, 167, 69)"
        self.error_style = "color: red"
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.resetColor)
        
    def setText(self, text: str) -> None:
        super().setText(text)
        if text:  # Only highlight if text is not empty
            self.setStyleSheet(self.highlight_style)
            self._timer.start(1000)
    
    def setSuccess(self, text: str) -> None:
        super().setText(text)
        if text:
            self.setStyleSheet(self.success_style)
            self._timer.stop()
    
    def setError(self, text: str) -> None:
        super().setText(text)
        if text:
            self.setStyleSheet(self.error_style)
            self._timer.stop()
    
    def resetColor(self):
        self.setStyleSheet(self.default_style)

class HighlightPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_palette = self.palette()
        self.default_style = self.styleSheet()
        self.highlight_style = "color: yellow;"  # Apply text color
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.resetColor)
        
    def setPlainText(self, text: str) -> None:
        super().setPlainText(text)
        if text:  # Only highlight if text is not empty
            self.setStyleSheet(self.highlight_style)
            self._timer.start(1000)
    
    def resetColor(self):
        self.setStyleSheet(self.default_style)