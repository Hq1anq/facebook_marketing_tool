from PySide6.QtCore import Qt

import src.settings as settings
from src.manager import DataManager
from src.gui.widget.ui_interface import Ui_MainWindow

class GetUI:
    def __init__(self, ui: Ui_MainWindow, data_manager: DataManager):
        self.ui = ui
        self.data_manager = data_manager