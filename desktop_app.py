import sys
import threading

from qr_wrapper import start_qt_app
from web_app import app


if __name__ == '__main__':
    app_thread = threading.Thread(
        target=app.run,
        daemon=True
    )
    app_thread.start()

    start_qt_app('localhost', 8050)