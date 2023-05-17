function formatSizeUnits(bytes){
  if      (bytes >= 1073741824) { bytes = (bytes / 1073741824).toFixed(2) + " GB"; }
  else if (bytes >= 1048576)    { bytes = (bytes / 1048576).toFixed(2) + " MB"; }
  else if (bytes >= 1024)       { bytes = (bytes / 1024).toFixed(2) + " KB"; }
  else if (bytes > 1)           { bytes = bytes + " bytes"; }
  else if (bytes == 1)          { bytes = bytes + " byte"; }
  else                          { bytes = "0 bytes"; }
  return bytes;
}
function loadJSON(callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', '../json/currentJson.json', true);
    xobj.onreadystatechange = function () {
      if (xobj.readyState === 4 && xobj.status === 200) {
        callback(JSON.parse(xobj.responseText));
      }
    };
    xobj.send(null);
  }
  loadJSON(function (jsonObject) {
    console.log(jsonObject["users"])
    const x = document.getElementById("files")
    let files = Object.keys(jsonObject['files'])
    console.log(files)
    for (let i = 0; i<files.length; i++){
        fileBytes=jsonObject["files"][files[i]]["total_bytes"]
        x.insertAdjacentHTML("beforeend","<tr><th>"+files[i]+"</th>"+"<th>"+formatSizeUnits(fileBytes)+"</th></tr>")
    }
    const y = document.getElementById("users")
    let users = Object.keys(jsonObject['users'])
    console.log(users)
    for (let i =0; i<users.length; i++){
      y.insertAdjacentHTML("beforeend","<tr><th>"+users[i]+"</th>"+"<th>"+jsonObject["users"][users[i]]["total"]+"</th></tr>")
    }
  });