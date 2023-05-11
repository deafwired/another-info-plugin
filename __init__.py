# Multiple parts of this are copied from Nachtalb's version of this,
# I just wanted to try and attempt to make it myself
from pynicotine.pluginsystem import BasePlugin
from pathlib import Path
import datetime
import json


JSONFORMAT = "Backup_%b_%d_%Y_%H_%M"


class Plugin(BasePlugin):
    def __init__(self):
        super().__init__()
        BASE_PATH = Path(__file__)
        self.log(f"Base path is {BASE_PATH}")
        self.jsonpath = BASE_PATH + "\\html\\json"

    def formatDate(self):
        now = datetime.datetime.now()
        return now.strftime("Backup_%b_%d_%Y_%H_%M")

    def download_finished_notification(self, user, virtual_path, real_path):
        try:
            pass
        except:
            with open(
                self.jsonpath + "\\" + self.formateDate(), "w", encoding="utf-8"
            ) as f:
                f.write()
                f.close()

    def log(self, *msg):
        super().log(*msg)
