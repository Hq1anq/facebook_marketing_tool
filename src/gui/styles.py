MENU_SELECTED_STYLE = """
    border-left: 14px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.416, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
    background-color: rgb(40, 44, 52);
    padding-left: 0px;
	text-align: left;
    """

MENU_NONE_SECLECTED_STYLE = """
    padding-left: 14px;
    text-align: left;
    border: none
    """

BUTTON_STYLE = """
    QPushButton {
        background-color: rgb(52, 59, 72);
        border: 3px solid rgb(52, 59, 72);
        color: white;
        padding: 3px 15px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 15px;
    }
    QPushButton:hover {
        background-color: rgb(57, 65, 80);
    }
"""

LABEL_STYLE = """
    QLabel {
        font-size: 14px;
        color: #333;
    }
"""

LINE_EDIT_STYLE = """
    QLineEdit {
        border: 2px solid #ccc;
        border-radius: 5px;
        padding: 10px;
    }
    QLineEdit:focus {
        border: 2px solid #4CAF50;
    }
"""

TABLE_STYLE = """
    QTableWidget {
        border: 1px solid #ccc;
        gridline-color: #ccc;
    }
    QTableWidget::item {
        padding: 10px;
    }
"""