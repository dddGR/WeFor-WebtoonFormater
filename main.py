import sys
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication
from wefor import do_FormatWebtoon
from gui.wefor_gui import MainWidget


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('fav.ico'))
    window = MainWidget(callback=do_FormatWebtoon)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()