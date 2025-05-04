from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self, host, port):
        super().__init__()
        self.setWindowTitle('Анализатор социальных связей')
        self.setGeometry(100, 100, 800, 600)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(f'http://{host}:{port}'))
        self.setCentralWidget(self.browser)


def start_qt_app(host, port, argv):
    qt_app = QApplication(argv)
    window = MainWindow(host, port)
    window.show()
    return qt_app.exec_()
