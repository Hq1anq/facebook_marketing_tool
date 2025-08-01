from PySide6.QtWidgets import QLabel, QFileDialog, QVBoxLayout, QScrollArea
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize, Qt, QObject, Signal

class ImageViewer(QObject):
    
    # Định nghĩa signal tùy chỉnh phát ra khi show_images được gọi
    imagesShown = Signal()
    
    def __init__(self, scroll_area, widget):
        super().__init__()
        # Assign existing QScrollArea and its widget
        self.scroll_area = scroll_area
        self.scroll_area_widget = widget
        self.list_image = []

        # Check if the widget already has a layout
        if self.scroll_area_widget.layout() is None:
            # Set the vertical layout for images inside the widget
            self.sc_layout = QVBoxLayout(self.scroll_area_widget)
            self.scroll_area_widget.setLayout(self.sc_layout)
        else:
            # Use the existing layout if one already exists
            self.sc_layout = self.scroll_area_widget.layout()

        # Define the label width and height for scaling images
        self.labelwidth = scroll_area.width() - 27
        self.scroll_area_widget.resizeEvent = self.onResize
        self.imgLabels = []

    def show_images(self, list_image = [], use_dialog = True):
        
        # Chọn ảnh từ dialog
        if not use_dialog:
            self.list_image = list_image
        else:
            self.list_image, _ = QFileDialog.getOpenFileNames(None, "Select Images", "", "Images (*.png *.xpm *.jpg)")

        # Xóa các hình ảnh cũ trong layout
        while self.sc_layout.count():
            widget_to_remove = self.sc_layout.takeAt(0).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()
        
        if not self.list_image:
            label = QLabel()
            label.setText("No images selected")
            self.sc_layout.addWidget(label)
            return

        # Hiển thị ảnh
        self.imgLabels.clear()
        try:
            for img in self.list_image:
                photo = QPixmap(img)

                original_width = photo.width()
                original_height = photo.height()

                # Scale
                scaled_height = int(self.labelwidth * original_height / original_width)
                scaled_photo = photo.scaled(QSize(self.labelwidth, scaled_height), Qt.KeepAspectRatio)

                # Tạo QLabel để hiển thị ảnh
                label = QLabel()
                label.setFixedSize(self.labelwidth, scaled_height)
                label.setPixmap(scaled_photo)

                # thêm Qlabel vừa tạo vào sc_layout
                self.sc_layout.addWidget(label)
                self.imgLabels.append((label, photo))
        except: pass
        # Gọi onResize để đảm bảo ảnh được điều chỉnh đúng kích thước
        self.onResize(None)
        
        # Phát ra signal imagesShown sau khi hiển thị ảnh
        self.imagesShown.emit()
        
    def onResize(self, event):
        # Get the new width of the QScrollArea
        new_width = self.scroll_area.width() - 27

        # Update the width of the labels dynamically
        try:
            for label, original_photo in self.imgLabels:
                original_width = original_photo.width()
                original_height = original_photo.height()

                # Calculate the new scaled height based on the new width
                scaled_height = int(new_width * original_height / original_width)

                # Scale the original image to the new width
                scaled_photo = original_photo.scaled(QSize(new_width, scaled_height), Qt.KeepAspectRatio)

                # Update the QLabel's size and pixmap
                label.setFixedSize(new_width, scaled_height)
                label.setPixmap(scaled_photo)

            # Call the base class resize event (optional)
            super(QScrollArea, self.scroll_area).resizeEvent(event)
        except: pass