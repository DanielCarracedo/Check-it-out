from PyQt5.QtWidgets import QApplication
from UI.Login import Loginw
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Loginw()
    login_window.show()
    sys.exit(app.exec_())