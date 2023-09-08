import app.secret as secret
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Create handlers
s_handler = logging.StreamHandler()
f_handler = logging.FileHandler('main.log')
s_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.INFO)
# Create formatters and add it to handlers
s_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
s_handler.setFormatter(s_format)
f_handler.setFormatter(f_format)
# Add handlers to the logger
logger.addHandler(s_handler)
logger.addHandler(f_handler)


class LabelLogging(logging.Handler):
    '''Класс для вывода логов в статусбар'''

    def __init__(self, lbl) -> None:
        logging.Handler.__init__(self)
        self.lbl = lbl

    def emit(self, record) -> None:
        msg = self.format(record)
        def set_log():
            self.lbl.config(text=msg)
        self.lbl.after(0, set_log)


DB = 'sql' #DB could be xls or sql
VIDEO = 0 #'rtsp://login:password@IP/'
PORT = 'COM3' #'COM5'
BAUD = 9600
BOT_TOKEN = secret.BOT_TOKEN
CHAT_IDS = secret.CHAT_IDS
