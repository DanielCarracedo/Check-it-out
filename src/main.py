from PyQt5.QtWidgets import QApplication
from UI.Login import Login
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    login_window.show()
    sys.exit(app.exec_())