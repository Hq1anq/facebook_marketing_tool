from PySide6.QtWidgets import QLabel, QPlainTextEdit
from PySide6.QtCore import QTimer, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter
from PySide6.QtSvg import QSvgRenderer


class HighlightLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.default_style = self.styleSheet()
        self.highlight_style = "color: yellow"
        self.success_style = "color: rgb(40, 167, 69)"
        self.error_style = "color: red"

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.resetColor)

        # ===== spinner state =====
        self._loading = False
        self._angle = 0

        # SVG icon (resource của bạn)
        self.renderer = QSvgRenderer(":/icons/icons/spinner.svg")

        # animation
        self.anim = QPropertyAnimation(self, b"angle")
        self.anim.setStartValue(0)
        self.anim.setEndValue(360)
        self.anim.setDuration(1000)
        self.anim.setLoopCount(-1)
        self.anim.setEasingCurve(QEasingCurve.Type.Linear)

    # ===== LOADING =====
    def setLoading(self, text: str):
        self._loading = True
        super().setText(text)
        self.resetColor()
        self._timer.stop()

        self.anim.start()
        self.update()

    # ===== SUCCESS =====
    def setSuccess(self, text: str):
        self._loading = False
        self.anim.stop()

        super().setText(text)
        self.setStyleSheet(self.success_style)
        self._timer.stop()

        self.update()

    # ===== ERROR =====
    def setError(self, text: str):
        self._loading = False
        self.anim.stop()

        super().setText(text)
        if text:
            self.setStyleSheet(self.error_style)
            self._timer.stop()

        self.update()

    # ===== DEFAULT TEXT =====
    def setText(self, text: str) -> None:
        self._loading = False
        self.anim.stop()

        super().setText(text)
        if text:
            self.setStyleSheet(self.highlight_style)
            self._timer.start(1000)

        self.update()

    # ===== RESET =====
    def resetColor(self):
        self.setStyleSheet(self.default_style)

    # ===== DRAW =====
    def paintEvent(self, event):
        if not self._loading:
            return super().paintEvent(event)

        painter = QPainter(self)

        # draw spinner
        size = 34
        margin = 6

        painter.save()
        painter.translate(margin + size / 2, self.height() / 2)
        painter.rotate(self._angle)
        painter.translate(-size / 2, -size / 2)

        self.renderer.render(painter, 
            QRectF(0, 0, size, size)
        )

        painter.restore()

        # draw text (dịch sang phải để chừa chỗ icon)
        painter.drawText(
            margin * 2 + size,
            0,
            self.width(),
            self.height(),
            self.alignment(),
            self.text()
        )

    # ===== ANIMATION PROPERTY =====
    def getAngle(self):
        return self._angle

    def setAngle(self, value):
        self._angle = value
        self.update()

    angle = Property(float, getAngle, setAngle)

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
