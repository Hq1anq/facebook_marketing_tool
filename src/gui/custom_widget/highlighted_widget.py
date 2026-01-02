from PySide6.QtWidgets import QLabel, QPlainTextEdit
from PySide6.QtCore import QTimer, Property, QPropertyAnimation, QEasingCurve, QRectF, Qt
from PySide6.QtGui import QFontMetrics, QPainter
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
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        margin = 4
        size = self.height() - (margin * 2)

        # ===== measure text =====
        fm = QFontMetrics(self.font())
        text_width = fm.horizontalAdvance(self.text())

        spacing = margin
        total_width = size + spacing + text_width

        # ===== compute start X based on alignment =====
        if self.alignment() & Qt.AlignmentFlag.AlignHCenter:
            start_x = (self.width() - total_width) / 2
        elif self.alignment() & Qt.AlignmentFlag.AlignRight:
            start_x = self.width() - total_width - margin
        else:
            start_x = margin

        icon_x = start_x
        text_x = icon_x + size + spacing

        # ===== draw spinner =====
        painter.save()
        painter.translate(icon_x + size / 2, self.height() / 2)
        painter.rotate(self._angle)
        self.renderer.render(
            painter,
            QRectF(-size / 2, -size / 2, size, size)
        )
        painter.restore()

        # ===== draw text =====
        painter.drawText(
            QRectF(text_x, 0, text_width, self.height()),
            Qt.AlignmentFlag.AlignVCenter,
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
