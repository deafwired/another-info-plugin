import json
import re
import os
from itertools import islice


class makeHTML:
    def __init__(self, data, template, PATH):
        self.data = data
        self.template = template
        topFiveUsers, topFiveFiles = self.topFive(self.data)
        x = template.readlines()
        files = list(data["files"].keys())
        for i in range(len(topFiveFiles)):
            text = (
                "          <li>"
                + self.stripPath(list(topFiveFiles.keys())[i])
                + "<span class='topFive'>" +
                str(list(topFiveFiles.values())[i])+"</span></li>\n"
            )
            x.insert(32 + i, text)
        x.pop(32 + len(topFiveFiles))
        for i in range(len(topFiveUsers)):
            text = (
                "          <li>"
                + list(topFiveUsers.keys())[i]
                + "<span class='topFive'>"
                + str(list(topFiveUsers.values())[i])
                + "</span></li>\n"
            )
            x.insert(38 + len(topFiveFiles) + i, text)
        x.pop(37 + len(topFiveFiles))
        for i in range(len(data["files"])):
            downloads = data["files"][files[i]]["count"]
            totalBytes = data["files"][files[i]]["total_bytes"]
            fileBytes = data["files"][files[i]]["bytes"]
            lastUser = data["files"][files[i]]["last_user"]
            href = "#" + lastUser
            text = (
                "        <tr><td>"
                + self.stripPath(files[i])
                + "</td><td>"
                + str(downloads)
                + '</td><td bytes="'
                + str(totalBytes)
                + '">'
                + self.bytesToStr(totalBytes)
                + '</td><td bytes="'
                + str(fileBytes)
                + '">'
                + self.bytesToStr(fileBytes)
                + "</td><td>"
                + "<a href="
                + href
                + ">"
                + lastUser
                + "</a></td></tr>\n"
            )
            x.insert(51 + len(topFiveFiles)+ len(topFiveUsers) + i, text)
        x.pop(51 + len(topFiveFiles) + len(topFiveUsers) + len(data["files"]))
        users = list(data["users"].keys())
        for i in range(len(data["users"])):
            downloads = data["users"][users[i]]["total"]
            totalBytes = data["users"][users[i]]["total_bytes"]
            last_file = data["users"][users[i]]["last_file"]
            # i love writing html in python, it just looks so clean and simple
            text = (
                "        <tr><td id='"
                + users[i]
                + "'>"
                + users[i]
                + "</td><td>"
                + str(downloads)
                + '</td><td bytes="'
                + str(totalBytes)
                + '">'
                + self.bytesToStr(totalBytes)
                + "</td><td>"
                + self.stripPath(last_file)
                + "</td></tr>\n"
            )
            x.insert(65 + len(topFiveFiles) + len(topFiveUsers) + len(data["files"]) + i, text)
        x.pop(65 + len(topFiveFiles) + len(topFiveUsers) + len(data["files"]) + len(data["users"]))

        with open(os.path.join(PATH, "index.html"), "w") as f:
            f.writelines(x)
            f.close()

    def stripPath(self, path):
        windowsStrip = re.compile(r".+\\")
        windowPath = windowsStrip.sub("", path)
        unixStrip = re.compile(r".+/")
        unixPath = unixStrip.sub("", windowPath)
        if len(unixPath) > len(windowPath):
            return windowPath
        return unixPath

    def topFive(self, data):
        users = {}
        for i in data["users"]:
            users[i] = data["users"][i]["total"]
        topFiveUsers = dict(
            sorted(users.items(), key=lambda x: x[1], reverse=True))
        files = {}
        for i in data["files"]:
            files[i] = data["files"][i]["count"]
        topFiveFiles = dict(
            sorted(files.items(), key=lambda x: x[1], reverse=True))
        return dict(islice(topFiveUsers.items(), 5)), dict(islice(topFiveFiles.items(), 5))

    def bytesToStr(self, num):
        units = ["Bytes", "KB", "MB", "GB", "TB"]
        unit_index = 0
        while num >= 1024 and unit_index < len(units) - 1:
            num /= 1024
            unit_index += 1
        formatted_value = "{:.2f}".format(num)
        return f"{formatted_value} {units[unit_index]}"



