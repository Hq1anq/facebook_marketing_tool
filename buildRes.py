import subprocess
import sys
from pathlib import Path

UI_FILE = Path("src/gui/widget/ui_interface.py")


def run_rcc():
    command = [
        "pyside6-rcc",
        "resources/resources.qrc",
        "-o",
        "resources/resources_rc.py"
    ]

    try:
        subprocess.run(command, check=True)
        print("✅ resources_rc.py generated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while running pyside6-rcc: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ pyside6-rcc not found. Make sure PySide6 is installed and in PATH.")
        sys.exit(1)


def patch_ui_file():
    if not UI_FILE.exists():
        print(f"❌ File not found: {UI_FILE}")
        return

    content = UI_FILE.read_text(encoding="utf-8")

    replacements = {
        "self.status = QLabel(self.pageContainer)":
            "self.status = HighlightLabel(self.pageContainer)",

        "self.cookieInput = QPlainTextEdit(self.useCookie)":
            "self.cookieInput = HighlightPlainTextEdit(self.useCookie)",

        "import resources_rc":
            "from src.gui.custom_widget.highlighted_widget import HighlightLabel, HighlightPlainTextEdit\n\nimport resources.resources_rc"
    }

    changed = False

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print(f"✔ Replaced: {old} -> {new}")
            changed = True

    if changed:
        UI_FILE.write_text(content, encoding="utf-8")
        print("✅ ui_interface.py updated!")
    else:
        print("ℹ No changes needed (already patched?)")


if __name__ == "__main__":
    run_rcc()
    patch_ui_file()