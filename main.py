from gui import MainWindow
from editor import Editor
import sys
from PySide6.QtWidgets import (
    QApplication, 
)

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    editor = Editor()
    window = MainWindow(editor)
    window.show()
    sys.exit(app.exec())