import glob
import os
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

    qt_exec_res = start_qt_app('localhost', 8050, sys.argv)
    [os.remove(f) for f in glob.glob('assets/graph_image_*.png')]
    [os.remove(f) for f in glob.glob('tables/metrics_*.csv')]
    sys.exit(qt_exec_res)
