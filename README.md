# Конфигурация

```python
# config.py
import os

ACCESS_TOKEN = 'YOUR_SERVICE_TOKEN'
APPDATA = os.path.expanduser('~') + '\\AppData\\Roaming\\sna_app'
ASSETS = APPDATA + '/assets'
TABLES = APPDATA + '/tables'
DUMPS = APPDATA + '/dumps'
```