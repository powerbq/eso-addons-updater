#!/usr/bin/python3

import os
import sys

_file_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)
_file_directory = os.path.dirname(_file_path)
_bundle_directory = getattr(sys, '_MEIPASS', _file_directory)
os.chdir(_file_directory)

from PyQt6.QtCore import QUrl
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtWebEngineQuick import QtWebEngineQuick
from PyQt6.QtWidgets import QApplication

from backend import Backend

if __name__ == '__main__':
    if sys.platform == 'win32':
        os.environ.setdefault('QT_QUICK_CONTROLS_STYLE', 'Fusion')

    QtWebEngineQuick.initialize()
    app = QApplication(sys.argv)
    backend = Backend()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('backend', backend)
    engine.load(QUrl.fromLocalFile(os.path.join(_bundle_directory, 'qml/main.qml')))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
