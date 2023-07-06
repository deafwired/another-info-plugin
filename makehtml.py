import os
import re
from itertools import islice


class makeHTML:
    def __init__(self, data, template, PATH):
        self.data = data
        topFiveUsers, topFiveFiles = self.topFive(self.data)
        # have to make a coy because otherwise you cant run the command more than once
        self.htmlLines = template[:]
        for i in range(len(self.htmlLines)):
            if "{TOPFILES}" in self.htmlLines[i]:
                self.topFiles(i, topFiveFiles)
                w = i
                break
        for i in range(w, len(self.htmlLines)):
            if "{TOPUSERS}" in self.htmlLines[i]:
                self.topUsers(i, topFiveUsers)
                w = i
                break
        for i in range(w, len(self.htmlLines)):
            if "{FILETABLE}" in self.htmlLines[i]:
                self.addSongs(i, self.data["files"])
                w = i
                break
        for i in range(w, len(self.htmlLines)):
            if "{USERTABLE}" in self.htmlLines[i]:
                self.addUser(i, self.data["users"])
        # deleting the template tags
        tags = ["{TOPFILES}", "{TOPUSERS}", "{FILETABLE}", "{USERTABLE}"]
        for tag in tags:
            for i in range(len(self.htmlLines)):
                if tag in self.htmlLines[i]:
                    self.htmlLines.pop(i)
                    break
        # writing the html file
        with open(os.path.join(PATH, "test.html"), "w") as f:
            f.writelines(self.htmlLines)
            f.close()

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
            totalBytes = data[i]["total_bytes"]
            last_file = data[i]["last_file"]
            # i love writing html in python, it just looks so clean and simple
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
