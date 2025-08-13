from PySide6.QtWidgets import QHeaderView, QTableWidgetItem, QFrame, QGraphicsDropShadowEffect, QLineEdit, QStyledItemDelegate, QStyleOptionViewItem
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QModelIndex
from PySide6.QtGui import QShortcut, QKeySequence, QColor, QPainter, QFont, QFontMetrics

from src.gui.widget.ui_tableWidget import Ui_tableWidget
from src.settings import TIME_ANIMATION

class TableWidget(QFrame, Ui_tableWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        
        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.contentFrame.setGraphicsEffect(self.shadow)
        
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(TIME_ANIMATION)  # Duration in milliseconds
        
        self.setup_filter_row()
        
        # Remove style of item in table for not overwite when setting background
        self.table.setStyleSheet(
            """QTableCornerButton::section { background-color: rgb(33, 37, 43) }
            QTableWidget {
                padding: 5px;
                gridline-color: rgb(44, 49, 58);
                border-bottom: 1px solid rgb(44, 49, 60); }
            QTableWidget::item:selected{
                background-color: rgb(189, 147, 249);
                color: rgb(40, 44, 52);
            }
            QHeaderView { qproperty-defaultAlignment: AlignCenter }
            QHeaderView::section {
                background-color: rgb(33, 37, 43);
                border: 1px solid rgb(44, 49, 60);
                font-size: 15px }
            QLineEdit {
                background-color: rgb(50, 54, 62); /* slightly lighter/darker variant for edit mode */
                selection-background-color: rgb(189, 147, 249); /* background when highlight */
                selection-color: rgb(40, 44, 52); /* text color when selected */
            }
            """)
        
        self.table.setItemDelegateForColumn(3, StatusChipDelegate())
        
        self._highlighted_rows = set()
        self.visible_index = None
        self.deleted_rows = []
        
        self.closeBtn.clicked.connect(self.animated_close)
        self.btn_add.clicked.connect(self.add_empty_row)
        self.btn_delete.clicked.connect(self.delete_row)
        
        undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        undo_shortcut.activated.connect(self.undo_delete)
        
        self.table.itemSelectionChanged.connect(self.highlight_selected_row)
        
        self.adjust_column_width()
        
    def adjust_column_width(self):
        # Temporarily hide filter row
        self.table.setRowHidden(0, True)
        header = self.table.horizontalHeader()

        # Set columns 2, 3 to ResizeToContents (fixed, minimum size)
        for i in range(2, 4):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)
            self.table.resizeColumnToContents(i)
            self.table.setColumnWidth(i, self.table.columnWidth(i) + 10)  # Add extra width

        # Set last column 0, 1 to Stretch (expand with parent)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        # Show filter row again
        self.table.setRowHidden(0, False)
    
    def setup_filter_row(self):
        self.table.setRowCount(1)  # Ensure at least one row for filters
        self.table.setVerticalHeaderItem(0, QTableWidgetItem("")) # Filter row not have header label
        self.filter_edits = []
        for col in range(self.table.columnCount()):
            edit = QLineEdit()
            edit.setPlaceholderText("Filter")
            edit.setAlignment(Qt.AlignmentFlag.AlignCenter if col != 9 else Qt.AlignmentFlag.AlignLeft)
            edit.setStyleSheet("background-color: rgb(40, 44, 52);")
            edit.returnPressed.connect(self.filter_table)
            self.table.setCellWidget(0, col, edit)
            self.filter_edits.append(edit)
    
    def load_group_table(self, data: dict):
        """Load group data from data_manager and render to table"""
        self.table.setRowCount(1)  # Clear current content
        for group in data.get("GET", {}).get("GROUP", []):
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, self.table_item(group.get("link group", "")))
            self.table.setItem(row_position, 1, self.table_item(group.get("link post", "")))
            self.table.setItem(row_position, 2, self.table_item(group.get("name group", "")))
            self.table.setItem(row_position, 3, self.table_item(group.get("status", ""), "center"))
                
            self.table.setVerticalHeaderItem(row_position, QTableWidgetItem(str(row_position)))
    
    def filter_table(self):
        self.visible_index = 1
        header_labels = []
        for row in range(1, self.table.rowCount()):  # Skip filter row
            show_row = True
            for col, edit in enumerate(self.filter_edits):
                filter_text = edit.text().lower()
                item = self.table.item(row, col)
                if filter_text and (not item or filter_text not in item.text().lower()):
                    show_row = False
                    break
            
            # Show/hide row and update row counter
            if show_row:
                self.table.setRowHidden(row, False)
                header_labels.append(str(self.visible_index))
                self.visible_index += 1
            else:
                self.table.setRowHidden(row, True)
                header_labels.append("")

        self.table.setVerticalHeaderLabels(header_labels)
        self.adjust_column_width()
        self.countRows.setText(f"Selected: {len(set(idx.row() for idx in self.table.selectedIndexes() if idx.row() > 0))}    Total rows: {self.visible_index if self.visible_index else self.table.rowCount()}")
                
    def highlight_selected_row(self):
        selected_rows = set(idx.row() for idx in self.table.selectedIndexes() if idx.row() > 0)
        
        # Rows to clear: previously highlighted but not currently selected
        rows_to_clear = self._highlighted_rows - selected_rows
        for row in rows_to_clear:
            for col in range(self.table.columnCount()):
                widget = self.table.cellWidget(row, col)
                if widget:
                    widget.setStyleSheet("")  # Clear highlight
                else:
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(QColor(40, 44, 52))  # Default bg
        
        # Rows to highlight: currently selected but not previously highlighted
        for row in selected_rows:
            for col in range(self.table.columnCount()):
                widget = self.table.cellWidget(row, col)
                if widget:
                    widget.setStyleSheet("background-color: #313640")  # Match highlight
                else:
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(QColor("#313640"))  # Subtle highlight

        # Update the cache
        self._highlighted_rows = selected_rows
        self.countRows.setText(f"Selected: {len(selected_rows)}     Total rows: {self.visible_index if self.visible_index else self.table.rowCount()}")
    
    def add_row(self, link: str, name: str):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, self.table_item(link))
        self.table.setItem(row_position, 1, self.table_item(""))
        self.table.setItem(row_position, 2, self.table_item(name))
        self.table.setItem(row_position, 3, self.table_item(""))
        self.table.setVerticalHeaderItem(row_position, QTableWidgetItem(str(row_position)))
    
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
                self.btn_run.setText("COMMENT")
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
                
    def table_item(self, text: str, align: str = "left"):
        item = QTableWidgetItem(text)
        if align == "left":
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        if align == "center":
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

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
    
    def add_empty_row(self):
        new_row_idx = self.table.rowCount()
        self.table.insertRow(new_row_idx)
        for i in range(4):
            self.table.setItem(new_row_idx, i, self.table_item(""))

    def delete_row(self):
        if self.table.rowCount() > 1:
            selectedRows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)
            for current_row in selectedRows:
                if current_row != 0:
                    row_data = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(current_row, col)
                        row_data.append(item.clone() if item else None)  # clone item for safety
                    self.deleted_rows.append((current_row, row_data))
                    self.table.removeRow(current_row)

    def undo_delete(self):
        if self.deleted_rows:
            row_index, row_data = self.deleted_rows.pop()
            self.table.insertRow(row_index)
            for col, value in enumerate(row_data):
                self.table.setItem(row_index, col, value)
            self.table.setVerticalHeaderItem(row_index, QTableWidgetItem(str(row_index)))

    def animated_close(self):
        """Animate widget shrinking and then close"""
        self.hide()
        return
        self.animation.setStartValue(self.geometry())  # Start at current size

        # Shrink towards the center
        center_x = self.x() + self.width() // 2
        center_y = self.y() + self.height() // 2
        self.animation.setEndValue(QRect(center_x, center_y, 0, 0))
        # animation.setEasingCurve(QEasingCurve.InOutQuart)

        self.setGraphicsEffect(None)
        self.animation.start()
        self.animation.finished.connect(self.hide)  # Hide after animation ends

class StatusChipDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        status = index.data(Qt.ItemDataRole.DisplayRole)
        
        if not status:  # Handle None or empty
            super().paint(painter, option, index)
            return
        
        status_lower = status.lower()

        status_styles = {
            "đã post": ("#16a34a", "white"),
            "đã comment": ("#eab308", "black"),
            "chưa post": ("#dc2626", "white"),
            "chưa comment": ("#dc2626", "white"),
            "không phải nhóm vps/proxy": ("#eab308", "black"),
            "bị chặn": ("#dc2626", "white"),
            "unknow": ("#6b7280", "white")
        }

        bg_color, text_color = status_styles.get(status_lower, status_styles["unknow"])

        # Let table draw selection background first
        super().paint(painter, option, index)

        # Draw the chip
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing) # Khử răng cưa

        # Font setup
        font = QFont(option.font)
        font.setPointSize(10)
        painter.setFont(font)
        metrics = QFontMetrics(font)

        # Text size + padding
        text_width = metrics.horizontalAdvance(status)
        text_height = metrics.height()
        padding_x = 8
        padding_y = 2
        chip_width = text_width + padding_x * 2
        chip_height = text_height + padding_y * 2

        # Center chip in cell
        cell_rect = option.rect
        chip_rect = QRect(
            cell_rect.x() + (cell_rect.width() - chip_width) // 2,
            cell_rect.y() + (cell_rect.height() - chip_height) // 2,
            chip_width,
            chip_height
        )

        # Draw chip background
        painter.setBrush(QColor(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(chip_rect, 10, 10)

        # Draw chip text
        painter.setPen(QColor(text_color))
        painter.drawText(chip_rect, Qt.AlignmentFlag.AlignCenter, status)

        painter.restore()
    '''
    Double-click cell
    ↓
    createEditor()         ← make QLineEdit
    ↓
    setEditorData()        ← fill QLineEdit with current cell value
    ↓  [user edits text]
    setModelData()         ← save new text back to model
    ↓
    paint()                ← draw updated cell (with chip)
    '''
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 👈 Center text while editing
        return editor 

    def setEditorData(self, editor, index):
        value = index.data(Qt.ItemDataRole.DisplayRole) or ""
        editor.setText(value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)