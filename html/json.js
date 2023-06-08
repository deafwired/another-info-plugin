function formatSizeUnits(bytes) {
  if (bytes >= 1073741824) {
    bytes = (bytes / 1073741824).toFixed(2) + " GB";
  } else if (bytes >= 1048576) {
    bytes = (bytes / 1048576).toFixed(2) + " MB";
  } else if (bytes >= 1024) {
    bytes = (bytes / 1024).toFixed(2) + " KB";
  } else if (bytes > 1) {
    bytes = bytes + " bytes";
  } else if (bytes == 1) {
    bytes = bytes + " byte";
  } else {
    bytes = "0 bytes";
  }
  return bytes;
}
function stripPath(path) {
  const winRegex = new RegExp(".+\\\\");
  const unixRegex = new RegExp(".+/");
  if (path.replace(winRegex, "").length > path.replace(unixRegex, "").length) {
    return path.replace(unixRegex, "");
  }
  return path.replace(winRegex, "");
}
function loadJSON(callback) {
  var xobj = new XMLHttpRequest();
  xobj.overrideMimeType("application/json");
  xobj.open("GET", "../json/currentJson.json", true);
  xobj.onreadystatechange = function () {
    if (xobj.readyState === 4 && xobj.status === 200) {
      callback(JSON.parse(xobj.responseText));
    }
  };
  xobj.send(null);
}
loadJSON(function (jsonObject) {
  console.log(jsonObject);
  const x = document.getElementById("files");
  let files = Object.keys(jsonObject["files"]);
  for (let i = 0; i < files.length; i++) {
    fileBytes = jsonObject["files"][files[i]]["bytes"];
    totalBytes = jsonObject["files"][files[i]]["total_bytes"];
    downloads = jsonObject["files"][files[i]]["count"];
    lastUser = jsonObject["files"][files[i]]["last_user"];
    link = encodeURI(files[i]);
    x.insertAdjacentHTML(
      "beforeend",
      "<tr><td><a href=file:///" +
        link +
        ">" +
        stripPath(files[i]) +
        "</td><td>" +
        downloads +
        '</td><td bytes="' +
        totalBytes +
        '">' +
        formatSizeUnits(totalBytes) +
        '</td><td bytes="' +
        fileBytes +
        '">' +
        formatSizeUnits(fileBytes) +
        "</td><td>" +
        lastUser +
        "</td></tr>"
    );
  }
  const y = document.getElementById("users");
  let users = Object.keys(jsonObject["users"]);
  for (let i = 0; i < users.length; i++) {
    totalFiles = jsonObject["users"][users[i]]["total"];
    totalSize = jsonObject["users"][users[i]]["total_bytes"];
    lastFile = jsonObject["users"][users[i]]["last_file"];
    y.insertAdjacentHTML(
      "beforeend",
      "<tr><td>" +
        users[i] +
        "</td>" +
        "<td>" +
        totalFiles +
        '</td><td bytes="' +
        totalSize +
        '">' +
        formatSizeUnits(totalSize) +
        "</td><td>" +
        stripPath(lastFile) +
        "</td></tr>"
    );
  }
  sortTableByBytes("filesHead", 2);
  sortTableByNumbers("usersHead", 1);
});
