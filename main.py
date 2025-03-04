# main.py
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets
import sys
from GUI.login import LoginWindow 

def init_app():
    app = QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = LoginWindow()  
    form.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    init_app()