# GUI/login.py
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox
from auth import login  # Import hàm login từ auth.py


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(625, 565)
        self.widget = QtWidgets.QWidget(parent=Form)
        self.widget.setGeometry(QtCore.QRect(30, 30, 550, 500))
        self.widget.setStyleSheet("QPushButton#pushButton{\n"
"    \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(11, 131, 120, 219), stop:0.55 rgba(85, 98,112, 226), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color:rgba(255,255,255,210);\n"
"border-radius: 5px;\n"
"}\n"
"QPushButton#pushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(150, 123, 120, 219), stop:0.55 rgba(85, 81,84, 226), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"}\n"
"QPushButton#pushButton:pressed{\n"
"    padding-left: 5px;\n"
"    padding-top:5px;\n"
"    background-color: rgba(150,123,111,255);\n"
"}\n"
"QPushButton#pushButton_2,#pushButton_3,#pushButton_4{\n"
"background-color:rgba(0,0,0,0);\n"
"color: rgba(85,98,112,255);\n"
"border:None\n"
"}\n"
"QPushButton#pushButton_2,#pushButton_3,#pushButton_4:hover{\n"
"color:rgba(131,96,53,255);\n"
"}\n"
"QPushButton#pushButton_2,#pushButton_3,#pushButton_4:pressed{\n"
"    padding-left: 5px;\n"
"    padding-top:5px;\n"
"    color:rgba(91,88,53,255);\n"
"}")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(parent=self.widget)
        self.label.setGeometry(QtCore.QRect(20, 30, 251, 430))
        self.label.setStyleSheet("background-color: rgba(0,0,0,80);\n"
"border-top-left-radius: 55px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.widget)
        self.label_2.setGeometry(QtCore.QRect(210, 30, 311, 431))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgba(255,255,255, 255);\n"
"border-bottom-right-radius: 50px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.widget)
        self.label_3.setGeometry(QtCore.QRect(340, 60, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgba(0,0,0,200)")
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(295, 150, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"border: none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color: rgab(0,0,0,240);\n"
"padding-bottom: 7px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(295, 215, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"border: none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color: rgab(0,0,0,240);\n"
"padding-bottom: 7px;")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton.setGeometry(QtCore.QRect(295, 280, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton#pushButton{\n"
"    \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(11, 131, 120, 219), stop:0.55 rgba(85, 98,112, 226), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color:rgba(255,255,255,210);\n"
"border-radius: 5px;\n"
"}\n"
"QPushButton#pushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(150, 123, 120, 219), stop:0.55 rgba(85, 81,84, 226), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"}\n"
"QPushButton#pushButton:pressed{\n"
"    padding-left: 5px;\n"
"    padding-top:5px;\n"
"    background-color: rgba(150,123,111,255);\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(parent=self.widget)
        self.label_4.setGeometry(QtCore.QRect(295, 340, 190, 16))
        self.label_4.setStyleSheet("color:rgba(0,0,0,210)")
        self.label_4.setObjectName("label_4")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(290, 360, 190, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton#pushButton_2{\n"
"background-color:rgba(0,0,0,0);\n"
"color: rgba(85,98,112,255);\n"
"}\n"
"QPushButton#pushButton_2:hover{\n"
"color:rgba(131,96,53,255);\n"
"}\n"
"QPushButton#pushButton_2:pressed{\n"
"    padding-left: 5px;\n"
"    padding-top:5px;\n"
"    color:rgba(91,88,53,255);\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("QPushButton#pushButton_2{\n"
"background-color:rgba(0,0,0,0);\n"
"color: rgba(85,98,112,255);\n"
"}\n"
"QPushButton#pushButton_2:hover{\n"
"color:rgba(131,96,53,255);\n"
"}\n"
"QPushButton#pushButton_2:pressed{\n"
"    padding-left: 5px;\n"
"    padding-top:5px;\n"
"    color:rgba(91,88,53,255);\n"
"}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton#pushButton_2{\n"
"background-color:rgba(0,0,0,0);\n"
"color: rgba(85,98,112,255);\n"
"}\n"
"QPushButton#pushButton_2:hover{\n"
"color:rgba(131,96,53,255);\n"
"}\n"
"QPushButton#pushButton_2:pressed{\n"
"    padding-left: 5px;\n"
"    padding-top:5px;\n"
"    color:rgba(91,88,53,255);\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.label_5 = QtWidgets.QLabel(parent=self.widget)
        self.label_5.setGeometry(QtCore.QRect(20, 80, 191, 201))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color:rgba(0,0,0,75);\n"
"")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=self.widget)
        self.label_6.setGeometry(QtCore.QRect(30, 80, 171, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:rgba(255,255,255,210\n"
")")
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "Log In"))
        self.lineEdit.setPlaceholderText(_translate("Form", "UserName"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Password"))
        self.pushButton.setText(_translate("Form", "Log In"))
        self.label_4.setText(_translate("Form", "Quên mật khẩu?"))
        self.pushButton_2.setText(_translate("Form", "E"))
        self.pushButton_4.setText(_translate("Form", "D"))
        self.pushButton_3.setText(_translate("Form", "C"))
        self.label_6.setText(_translate("Form", "MikeDang\'s Clinic "))


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Login")

        # Kết nối nút Login với hàm xử lý
        self.ui.pushButton.clicked.connect(self.handle_login)

    def handle_login(self):
        # Lấy dữ liệu từ input
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        # Gọi hàm login từ auth.py
        role = login(username, password)

        if role:
            # Đăng nhập thành công, điều hướng sang interface
            self.open_dashboard(role)
        else:
            # Đăng nhập thất bại, hiển thị thông báo lỗi
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def open_dashboard(self, role):
        # Đóng giao diện login và mở dashboard
        from GUI.interface import DashboardWindow
        self.dashboard = DashboardWindow(role)
        self.dashboard.show()
        self.close()


# Để kiểm tra riêng lẻ
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())