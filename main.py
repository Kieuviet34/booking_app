# main.py
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets
import sys
from GUI.login import Ui_Form  

def init_app():
    app = QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(form)  
    form.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    init_app()