#Transfers the data from natchalbs to mine
import json

importFile = "PATHTONATCHALBSJSON" # the backup files in the html foldeer
exportFile = "..\\json\\currentJson.json"
Import = json.load(open(importFile, "r"))
try:
    Export = json.load(open(exportFile, "r"))
except:
    currentJson={
        "files":{},
        "users":{},
        "day":[0,0,0,0,0,0,0]
    }
for user in Import["user"]:
    try:
        Export["users"][user]["total"] += Import["user"][user]["total"]
        Export["users"][user]["total_bytes"] += Import["user"][user]["total_bytes"]
    except:
        Export["users"][user] = {}
        Export["users"][user]["total"] = Import["user"][user]["total"]
        Export["users"][user]["total_bytes"] = Import["user"][user]["total_bytes"]
        Export["users"][user]["last_file"] = Import["user"][user]["last_file"]
for file in Import["file"]:
    try:
        Export["files"][file]["count"] += Import["file"][file]["count"]
        Export["files"][file]["total_bytes"] += Import["file"][file]["total_bytes"]
    except:
        Export["files"][file] = {}
        Export["files"][file]["count"] = Import["file"][file]["total"]
        Export["files"][file]["bytes"] = Import["file"][file]["file_size"]
        Export["files"][file]["total_bytes"] = Import["file"][file]["total_bytes"]
        Export["files"][file]["last_user"] = Import["file"][file]["last_user"]
json.dump(Export, open(Export, "w"))