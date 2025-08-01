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
        background-color: #4CAF50; /* Green */
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #45a049;
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