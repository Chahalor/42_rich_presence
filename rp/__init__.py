# rp/__init__.py

from .config import config
from .start import start
from .status import status
from .stop import stop
from .connect import connect, update

MAIN_DIR:		str = "~/.rpc/"
SOCKET_PATH:	str = MAIN_DIR + "rich_presence.sock"
PID_FILE:		str = MAIN_DIR + "rich_presence.pid"
CONFIG_FILE:	str = MAIN_DIR + "config.json"

APP_ID:			str = "1408374003411849216"