import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from window import Window
import sys


def main():
    sys.setrecursionlimit(10000)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()