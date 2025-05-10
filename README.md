# Конфигурация

```python
# config.py
import os

APPDATA = os.path.expanduser('~') + '\\AppData\\Roaming\\sna_app'
TABLES = APPDATA + '/tables'
DUMPS = APPDATA + '/dumps'
```