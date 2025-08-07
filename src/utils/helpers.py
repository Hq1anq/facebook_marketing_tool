from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

def apply_int_range_validator(line_edit: QLineEdit, normalize: bool = True):
    """
    Applies a validator to a QLineEdit that only accepts:
    - A single integer (e.g. "16")
    - A range of integers with optional spaces (e.g. "5-8", "20 - 45")

    Optionally normalizes input to the format "int" or "int - int" after editing.

    Parameters:
        line_edit (QLineEdit): The QLineEdit to apply the rule to.
        normalize (bool): If True, formats the text on editingFinished.
    """
    regex = QRegularExpression(r"^\d+\s*(-\s*\d+)?$")
    validator = QRegularExpressionValidator(regex)
    line_edit.setValidator(validator)

    if normalize:
        def normalize_input():
            text = line_edit.text()
            parts = [x.strip() for x in text.split('-') if x.strip().isdigit()]
            if len(parts) == 1 and parts[0].isdigit():
                line_edit.setText(f"{parts[0]}")
            elif len(parts) == 2 and all(p.isdigit() for p in parts):
                line_edit.setText(f"{parts[0]} - {parts[1]}")
        line_edit.editingFinished.connect(normalize_input)

def is_file_open(file_path: str):
    try:
        file = open(file_path, "a")
        file.close()
        return False
    except:
        return True