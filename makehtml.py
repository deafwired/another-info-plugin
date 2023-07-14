import os
import re
from itertools import islice


class makeHTML:
    def __init__(self, data, template, PATH, limit):
        self.data = data
        self.limit = limit
        topFiveUsers, topFiveFiles = self.topFive(self.data)
        # have to make a copy because otherwise you cant run the command more than once
        self.htmlLines = template[:]
        # get topfiles
        for i in range(len(self.htmlLines)):
            if "{TOPFILES}" in self.htmlLines[i]:
                self.topFiles(i, topFiveFiles)
                w = i
                break
        # get topusers
        for i in range(w, len(self.htmlLines)):
            if "{TOPUSERS}" in self.htmlLines[i]:
                self.topUsers(i, topFiveUsers)
                w = i
                break
        # get summary
        for i in range(w, len(self.htmlLines)):
            if "{SUMMARY}" in self.htmlLines[i]:
                self.summary(i, self.data)
                w = i
                break
        # get weekday
        for i in range(w, len(self.htmlLines)):
            if "{WEEKDAY}" in self.htmlLines[i]:
                self.downloadsPerDay(i, self.data)
                w = i
                break
        # get filetable
        for i in range(w, len(self.htmlLines)):
            if "{FILETABLE}" in self.htmlLines[i]:
                self.addSongs(i, self.data["files"])
                w = i
                break
        # get usertable
        for i in range(w, len(self.htmlLines)):
            if "{USERTABLE}" in self.htmlLines[i]:
                self.addUser(i, self.data["users"])
        # deleting the template tags
        tags = [
            "{TOPFILES}",
            "{TOPUSERS}",
            "{SUMMARY}",
            "{WEEKDAY}",
            "{FILETABLE}",
            "{USERTABLE}",
        ]
        for tag in tags:
            for i in range(len(self.htmlLines)):
                if tag in self.htmlLines[i]:
                    self.htmlLines.pop(i)
                    break
        # writing the html file
        with open(os.path.join(PATH, "index.html"), "w") as f:
            f.writelines(self.htmlLines)
            f.close()

    def summary(self, pos, data):
        totalFiles = len(data["files"])
        totalUsers = len(data["users"])
        totalUploads = 0
        totalBytes = 0
        if len(data["users"]) > len(data["files"]):
            for i in data["users"]:
                totalUploads += data["users"][i]["total"]
                totalBytes += data["users"][i]["total_bytes"]
        else:
            for i in data["files"]:
                totalUploads += data["files"][i]["count"]
                totalBytes += data["files"][i]["total_bytes"]

        # i love writing html in python, it just looks so clean and simple
        text = (
            "        <dt>Number of files</dt>\n"
            + "        <dd>"
            + str(totalFiles)
            + "</dd>\n"
            + "        <dt>Number of users</dt>\n"
            + "        <dd>"
            + str(totalUsers)
            + "</dd>\n"
            + "        <dt>Total uploads</dt>\n"
            + "        <dd>"
            + str(totalUploads)
            + "</dd>\n"
            + "        <dt>Total bytes</dt>\n"
            + "        <dd>"
            + self.bytesToStr(totalBytes)
            + "</dd>\n"
        )
        self.htmlLines.insert(pos, text)

    def downloadsPerDay(self, pos, data):
        daysofweek = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        text = ""
        for i in range(len(data["day"])):
            percent = round(data["day"][i] / max(data["day"]), 4) * 100
            text += (
                "        <li style='--widthpercent:"
                + str(percent)
                + "%;'>"
                + str(data["day"][i])
                + "&emsp;"
                + str(daysofweek[i])
                + "</li>\n"
            )
        self.htmlLines.insert(pos, text)

    # add the top five files
    def topFiles(self, pos, data):
        keys = [self.stripPath(key) for key in data.keys()]
        items = list(data.values())
        for i in range(len(data)):
            text = (
                "          <li>"
                + str(keys[i])
                + "<span class='topFive'>"
                + str(items[i])
                + "</span></li>\n"
            )
            self.htmlLines.insert(pos + i, text)

    # add the top five users
    def topUsers(self, pos, data):
        keys = [key for key in data.keys()]
        items = list(data.values())
        for i in range(len(data)):
            text = (
                "          <li>"
                + str(keys[i])
                + "<span class='topFive'>"
                + str(items[i])
                + "</span></li>\n"
            )
            self.htmlLines.insert(pos + i, text)

    # add the songs to the table
    def addSongs(self, pos, data):
        for i in data:
            downloads = data[i]["count"]
            if downloads < self.limit:
                continue
            totalBytes = data[i]["total_bytes"]
            fileBytes = data[i]["bytes"]
            lastUser = data[i]["last_user"]
            href = "#" + lastUser
            text = (
                "        <tr><td>"
                + self.stripPath(i)
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
            self.htmlLines.insert(pos, text)

    # add the users to the table
    def addUser(self, pos, data):
        for i in data:
            downloads = data[i]["total"]
            if downloads < self.limit:
                continue
            totalBytes = data[i]["total_bytes"]
            last_file = data[i]["last_file"]
            text = (
                "        <tr><td id='"
                + i
                + "'>"
                + i
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
            self.htmlLines.insert(pos, text)

    # checks if the path is windows or unix and strips the path based on if its shorter
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
        topFiveUsers = dict(sorted(users.items(), key=lambda x: x[1], reverse=True))
        files = {}
        for i in data["files"]:
            files[i] = data["files"][i]["count"]
        topFiveFiles = dict(sorted(files.items(), key=lambda x: x[1], reverse=True))
        return dict(islice(topFiveUsers.items(), 5)), dict(
            islice(topFiveFiles.items(), 5)
        )

    def bytesToStr(self, num):
        units = ["Bytes", "KB", "MB", "GB", "TB"]
        unit_index = 0
        while num >= 1024 and unit_index < len(units) - 1:
            num /= 1024
            unit_index += 1
        formatted_value = "{:.2f}".format(num)
        return f"{formatted_value} {units[unit_index]}"
