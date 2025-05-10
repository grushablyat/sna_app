import glob
import os
import sys
import threading

from config import APPDATA, TABLES
from qr_wrapper import start_qt_app
from web_app import app


if __name__ == '__main__':
    app_thread = threading.Thread(
        target=app.run,
        daemon=True
    )
    app_thread.start()

    [os.mkdir(dir) for dir in (APPDATA, TABLES) if not os.path.exists(dir)]

    qt_exec_res = start_qt_app('localhost', 8050, sys.argv)

    [os.remove(f) for f in glob.glob(f'{TABLES}/metrics_*.csv')]

    sys.exit(qt_exec_res)
