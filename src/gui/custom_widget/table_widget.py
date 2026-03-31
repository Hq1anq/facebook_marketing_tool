from PySide6.QtWidgets import QHeaderView, QTableWidgetItem, QFrame, QGraphicsDropShadowEffect, QLineEdit, QStyledItemDelegate, QStyleOptionViewItem
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QModelIndex
from PySide6.QtGui import QShortcut, QKeySequence, QColor, QPainter, QFont, QFontMetrics

from src.manager import DataManager
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
        
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["LINK GROUP", "NAME GROUP", "LINK POST", "CONTENT", "STATUS"])
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
        
        self.table.setItemDelegateForColumn(4, StatusChipDelegate())
        
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
        
        self.current_mode = "POST" # Default
        
    def adjust_column_width(self):
        # Temporarily hide filter row
        self.table.setRowHidden(0, True)
        header = self.table.horizontalHeader()

        # Columns that stretch: 0, 2, 3 (LINKS, CONTENT)
        # Columns to ResizeToContents: 1, 4 (NAME GROUP, STATUS)
        for i in range(self.table.columnCount()):
            if not self.table.isColumnHidden(i):
                if i in [1, 4]:
                    header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)
                    self.table.resizeColumnToContents(i)
                    self.table.setColumnWidth(i, self.table.columnWidth(i) + 10)  # Add extra width
                else:
                    header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
        
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
    
    def load_table_data(self, data_list: list):
        """Load group/post data and render to table"""
        self.table.setRowCount(1)  # Clear current content keeping filter row
        
        # Clear existing spans
        self.table.clearSpans()
        
        for group in data_list:
            posts = group.get("posts", [])
            
            # Special logic for GET GROUP: Always one row per group
            if self.current_mode == "GET GROUP":
                self.add_row(
                    link_group=group.get("link group", ""),
                    name_group=group.get("name group", "")
                )
                continue

            # If no posts yet, display group as single row
            if not posts:
                self.add_row(
                    link_group=group.get("link group", ""),
                    name_group=group.get("name group", "")
                )
                continue
                
            start_row = self.table.rowCount()
            row_count = len(posts)
            
            for post in posts:
                # Select status based on current mode
                if self.current_mode == "COMMENT":
                    status = post.get("status_comment", "")
                else:
                    status = post.get("status_post", "")
                    
                self.add_row(
                    link_group=group.get("link group", ""),
                    name_group=group.get("name group", ""),
                    link_post=post.get("link post", ""),
                    content=post.get("content", ""),
                    status=status
                )
                
            # Merge group info if there are multiple posts
            if row_count > 1:
                self.table.setSpan(start_row, 0, row_count, 1) # Merge Link Group
                self.table.setSpan(start_row, 1, row_count, 1) # Merge Group Name
    
    
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
    
    def add_row(self, link_group: str = "", name_group: str = "", link_post: str = "", content: str = "", status: str = ""):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, self.table_item(link_group))
        self.table.setItem(row_position, 1, self.table_item(name_group))
        self.table.setItem(row_position, 2, self.table_item(link_post))
        self.table.setItem(row_position, 3, self.table_item(content))
        
        # Hide original status text by setting its color to background color
        status_item = self.table_item(status, "center", QColor(40, 44, 52))
        self.table.setItem(row_position, 4, status_item)
        
        self.table.setVerticalHeaderItem(row_position, QTableWidgetItem(str(row_position)))

    def insert_post_for_group(self, link_group: str = "", name_group: str = "", link_post: str = "", content: str = "", status: str = ""):
        start_row = -1
        span_count = 1
        
        for row in range(1, self.table.rowCount()):
            if self.get_cell_text(row, 0) == link_group:
                if start_row == -1:
                    start_row = row
                    span_count = self.table.rowSpan(row, 0)
                    if span_count <= 0:
                        span_count = 1
                
                # Deduplication check: if this post link already exists in this group's rows
                if self.get_cell_text(row, 2) == link_post:
                    print(f"DEBUG: Post {link_post} already exists in group {link_group}, skipping.")
                    return
                
        if start_row == -1:

            self.add_row(link_group, name_group, link_post, content, status)
            return

        # Check if the row is just an empty group row
        if span_count == 1:
            item_post = self.table.item(start_row, 2)
            if not item_post or not item_post.text().strip():
                self.table.setItem(start_row, 2, self.table_item(link_post))
                self.table.setItem(start_row, 3, self.table_item(content))
                self.table.setItem(start_row, 4, self.table_item(status, "center", QColor(40, 44, 52)))
                return

        # Insert new row beneath the group's span
        insert_row = start_row + span_count
        self.table.insertRow(insert_row)
        
        # We add the group info but "hide" it by setting color to background
        # This prevents the UI from showing duplicate text behind the span
        # but allows get_cell_text to find it if span logic is tricky
        self.table.setItem(insert_row, 0, self.table_item(link_group, "left", QColor(40, 44, 52)))
        self.table.setItem(insert_row, 1, self.table_item(name_group, "left", QColor(40, 44, 52)))
        self.table.setItem(insert_row, 2, self.table_item(link_post))
        self.table.setItem(insert_row, 3, self.table_item(content))
        self.table.setItem(insert_row, 4, self.table_item(status, "center", QColor(40, 44, 52)))

        
        new_span_count = span_count + 1
        self.table.setSpan(start_row, 0, new_span_count, 1)
        self.table.setSpan(start_row, 1, new_span_count, 1)
        
        # Refresh vertical headers across the rest of the table
        for r in range(start_row, self.table.rowCount()):
            self.table.setVerticalHeaderItem(r, QTableWidgetItem(str(r)))

    
    def setup(self, func: str):
        self.current_mode = func
        # Reset visibility before applying specific mode settings
        for i in range(self.table.columnCount()):
            self.table.setColumnHidden(i, False)

        match func:
            case "POST":
                self.btn_run.setText("POST")
                self.filterGroup.hide()
                self.fromLabel.setText("Từ group")
                self.toLabel.setText("đến group")
                self.listLabel.setText("List group")
                self.table.setColumnHidden(0, True) # Hide link group
                # table shows: NAME GROUP | LINK POST | CONTENT | STATUS

            case "COMMENT":
                self.btn_run.setText("COMMENT")
                self.filterGroup.hide()
                self.fromLabel.setText("Từ post")
                self.toLabel.setText("đến post")
                self.listLabel.setText("ListPost")
                self.table.setColumnHidden(0, True) # Hide link group
                self.table.setColumnHidden(2, True) # Hide link post
                # table shows: NAME GROUP | LINK POST | CONTENT | STATUS

            case "GET GROUP":
                self.btn_run.setText("GET GROUP")
                self.filterGroup.show()
                self.table.setColumnHidden(2, True) # Hide link post
                self.table.setColumnHidden(3, True) # Hide content
                self.table.setColumnHidden(4, True) # Hide status
                # table shows: LINK GROUP | NAME GROUP

            case "GET POST":
                self.btn_run.setText("GET POST")
                self.filterGroup.hide()
                self.fromLabel.setText("Từ group")
                self.toLabel.setText("đến group")
                self.listLabel.setText("List group")
                self.table.setColumnHidden(0, True) # Hide link group
                self.table.setColumnHidden(4, True) # Hide status
                # table shows: NAME GROUP | LINK POST | CONTENT
        
        self.adjust_column_width()
                
    def table_item(self, text: str, align: str = "left", color: QColor = None):
        item = QTableWidgetItem(text)
        # Always center vertically
        if align == "left":
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        elif align == "center":
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            
        if color:
            item.setForeground(color)
        return item

    def get_cell_text(self, row, col):
        """Safely extract text, accounting for spanned cells"""
        # 1. First, try to get the item directly at this cell
        item = self.table.item(row, col)
        if item and item.text().strip():
            return item.text().strip()

        # 2. If no direct text, check if this is part of a merge from a row above
        for r in range(row - 1, -1, -1):
            span = self.table.rowSpan(r, col)
            if span > 1 and (r + span > row):
                merge_root_item = self.table.item(r, col)
                return merge_root_item.text().strip() if merge_root_item else ""
        
        return ""

    def get_selected(self):
        # Correctly gather all selected row indexes
        selected_indexes = self.table.selectedIndexes()
        if not selected_indexes: return []
        
        selected_rows = sorted(set(idx.row() for idx in selected_indexes if idx.row() > 0))
        
        selected_items = []
        seen_group_links = set() # For deduplication in group modes

        if self.current_mode in ["POST", "GET POST", "GET GROUP"]:
            col = 1 # NAME GROUP
        elif self.current_mode == "COMMENT":
            col = 3 # CONTENT
        else: col = 1
        self.table.clearSelection()
        for row in selected_rows:
            item = self.table.item(row, col)
            if item:
                item.setSelected(True)
            # We must get the cell text carefully for each column
            lg = self.get_cell_text(row, 0)
            ng = self.get_cell_text(row, 1)
            lp = self.get_cell_text(row, 2)
            c = self.get_cell_text(row, 3)
            st = self.get_cell_text(row, 4)
            
            # If we are in a group-level operation mode (POST, GET POST, etc.)
            # we should avoid duplicate group links if the user selected multiple posts in one group
            if self.current_mode in ["POST", "GET POST", "GET GROUP"]:
                if lg in seen_group_links:
                    continue
                seen_group_links.add(lg)
                        
            item_data = {
                "row": row,
                "link group": lg,
                "name group": ng,
                "link post": lp,
                "content": c,
                "type_status": "status_post" if self.current_mode != "COMMENT" else "status_comment",
                "status": st
            }
            selected_items.append(item_data)
        
        print(f"DEBUG: Processed {len(selected_items)} selected items for {self.current_mode}")
        for i, item in enumerate(selected_items):
            print(f"  Item {i+1}: Group '{item['name group']}' | Row {item['row']}")
            
        return selected_items

    def save_table_data(self, data_manager: DataManager):
        """Save UI data corresponding to the used columns in current action back to data_manager"""
        original_table = data_manager.data.get("TABLE", [])
        new_table_data = []

        # Reconstruct group-post mapping top-to-bottom
        for row in range(1, self.table.rowCount()):
            lg = self.get_cell_text(row, 0)
            ng = self.get_cell_text(row, 1)
            lp = self.get_cell_text(row, 2)
            c = self.get_cell_text(row, 3)
            st = self.get_cell_text(row, 4)

            # Find or insert group
            group = next((g for g in new_table_data if g["link group"] == lg), None)
            if not group:
                group = {"link group": lg, "name group": ng, "posts": []}
                new_table_data.append(group)
                
                # If we're in GET GROUP or if this is the only row for this group (no post info yet)
                # we might want to preserve its historical posts from original_table.
                orig_g = next((g for g in original_table if g["link group"] == lg), None)
                if orig_g:
                    if self.current_mode == "GET GROUP":
                        group["posts"] = orig_g.get("posts", [])
                    elif not lp and not c:
                        # If this row in UI has no post data, but the original group had posts, 
                        # it means it's an empty group row in UI that should keep its data.
                        group["posts"] = orig_g.get("posts", [])

            # skip remaining logic for GET GROUP as it doesn't handle individual posts
            if self.current_mode == "GET GROUP":
                continue

            # Build post entry intelligently
            if lp or c:
                orig_g = next((g for g in original_table if g["link group"] == lg), None)
                orig_p = next((p for p in orig_g.get("posts", []) if p.get("link post") == lp), None) if orig_g else None

                post_data = {
                    "link post": lp,
                    "content": c,
                    "status_post": orig_p.get("status_post", "") if orig_p else "",
                    "status_comment": orig_p.get("status_comment", "") if orig_p else ""
                }

                if self.current_mode == "COMMENT":
                    post_data["status_comment"] = st
                elif self.current_mode in ["POST", "GET POST"]:
                    post_data["status_post"] = st

                # Only add if not already in this group's posts (prevents duplicate entries during save loop)
                if not any(p["link post"] == lp for p in group["posts"]):
                    group["posts"].append(post_data)


        # Update dict and trigger file save
        data_manager.data["TABLE"] = new_table_data
        success = data_manager.save_data()
        
        # if success:
        #     self.statusTable.setText("Đã lưu dữ liệu bảng vào " + data_manager.data_path)
        # else:
        #     self.statusTable.setText("Lỗi: không thể lưu dữ liệu")
            
    def finish_action(self, func: str, data_manager: DataManager):
        """Standard sequence triggered upon finishing any table action"""
        self.btn_run.setText(func)
        self.adjust_column_width()
        if func in ["GET GROUP", "GET POST", "POST", "COMMENT"]:
            self.save_table_data(data_manager)

    def add_empty_row(self):
        new_row_idx = self.table.rowCount()
        self.table.insertRow(new_row_idx)
        for i in range(5):
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
        self.statusTable.setText("")
        self.hide()
        return

class StatusChipDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        status = index.data(Qt.ItemDataRole.DisplayRole)
        
        if not status:  # Handle None or empty
            super().paint(painter, option, index)
            return
        
        status_lower = status.lower()

        status_styles = {
            "đã post": ("#1e7d4b", "#4dffa3"),
            "đã comment": ("#9a5b12", "#ffc861"),
            "chưa post": ("#922c3c", "#ff99a3"),
            "chưa comment": ("#922c3c", "#ff99a3"),
            "không phải nhóm vps/proxy": ("#9a5b12", "#ffc861"),
            "bị chặn": ("#922c3c", "#ff99a3"),
            "unknow": ("#6b7280", "white")
        }

        bg_color, text_color = status_styles.get(status_lower, status_styles["unknow"])

        # Let table draw selection background first
        super().paint(painter, option, index)

        # Draw the chip
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing) # Khử răng cưa

        # Font setup - reduce font size for very long text
        font = QFont(option.font)
        if len(status) > 20: 
            font.setPointSize(8)
        elif len(status) > 12:
            font.setPointSize(9)
        else:
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
        painter.drawRoundedRect(chip_rect, chip_height // 2, chip_height // 2)

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