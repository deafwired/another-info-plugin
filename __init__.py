# Multiple parts of this are copied from Nachtalb's version of this,
# I just wanted to try and attempt to make it myself
from pynicotine.pluginsystem import BasePlugin
from pathlib import Path
import datetime
import json
import os
import threading


JSONFORMAT = "Backup_%b_%d_%Y_%H_%M"


class Plugin(BasePlugin):
    def __init__(self):
        super().__init__()
        BASE_PATH = Path(__file__).parent
        self.jsonPath = os.path.join(BASE_PATH, "json")
        load = open(os.path.join(self.jsonPath, "currentJson.json"), "r")
        self.stats = json.load(load)
        load.close()
        self.log(f"{threading.enumerate()}")
        self.scheduling()

    def formatDate(self):
        now = datetime.datetime.now()
        return now.strftime("Backup_%b_%d_%Y_%H%M")

    def upload_finished_notification(self, user, virtual_path, real_path):
        try:
            self.stats["files"][real_path]["count"] += 1
            self.stats["files"][real_path]["total_bytes"] += self.stats["files"][real_path]["bytes"]
        except:
            self.stats["files"][real_path] = {}
            self.stats["files"][real_path]["count"] = 1
            self.stats["files"][real_path]["bytes"] = os.path.getsize(
                real_path)
            self.stats["files"][real_path]["total_bytes"] = self.stats["files"][real_path]["bytes"]
        self.stats["files"][real_path]["last_user"] = user
        try:
            self.stats["users"][user]["total"] += 1
            self.stats["users"][user]["last_file"] = real_path
            self.stats["users"][user]["total_bytes"] += os.path.getsize(
                real_path)
        except:
            self.stats["users"][user] = {}
            self.stats["users"][user]["total"] = 1
            self.stats["users"][user]["last_file"] = real_path
            self.stats["users"][user]["total_bytes"] = os.path.getsize(
                real_path)

    def saveJson(self, json_path, stats):
        path = json_path+"\\"+self.formatDate()+".json"
        f = open(path, "w")
        json.dump(stats, f)
        f.close()
        f = open(json_path+"\\currentJson.json", "w")
        json.dump(stats, f)
        f.close()

    def disable(self):
        self.log(f"unloading")
        self.timer.cancel()
        self.saveJson(self.jsonPath, self.stats)

    def scheduling(self, interval=3600):
        self.saveJson(self.jsonPath, self.stats)
        self.timer = threading.Timer(interval, self.scheduling, args=[interval])
        self.timer.start()

    def log(self, *msg):
        super().log(*msg)
