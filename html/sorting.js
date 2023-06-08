function sortTable(tableId, column) {
  var table = document.getElementById(tableId);
  var tbody = table.tBodies[0];
  var rows = Array.from(tbody.rows);

  rows.sort(function (a, b) {
    var aValue = a.cells[column].innerText;
    var bValue = b.cells[column].innerText;

    if (!isNaN(parseFloat(aValue)) && !isNaN(parseFloat(bValue))) {
      aValue = parseFloat(aValue);
      bValue = parseFloat(bValue);
    }

    if (aValue < bValue) {
      return -1;
    } else if (aValue > bValue) {
      return 1;
    } else {
      return 0;
    }
  });

  var fragment = document.createDocumentFragment();

  for (var i = 0; i < rows.length; i++) {
    fragment.appendChild(rows[i]);
  }

  tbody.appendChild(fragment);
}
function sortTableByBytes(tableId, column) {
  var table = document.getElementById(tableId);
  var tbody = table.tBodies[0];
  var rows = Array.from(tbody.rows);

  rows.sort(function (a, b) {
    var aValue = getByteValue(a.cells[column]);
    var bValue = getByteValue(b.cells[column]);

    return bValue - aValue;
  });

  var fragment = document.createDocumentFragment();

  for (var i = 0; i < rows.length; i++) {
    fragment.appendChild(rows[i]);
  }

  tbody.appendChild(fragment);
}
function getByteValue(cell) {
  var bytesAttr = cell.getAttribute('bytes');
  var bytes = parseFloat(bytesAttr);

  return bytes;
}
function sortTableByNumbers(tableId, column) {
  var table = document.getElementById(tableId);
  var tbody = table.tBodies[0];
  var rows = Array.from(tbody.rows);

  rows.sort(function (a, b) {
    var aValue = parseFloat(a.cells[column].innerText);
    var bValue = parseFloat(b.cells[column].innerText);

    return bValue - aValue; // Compare in descending order
  });

  var fragment = document.createDocumentFragment();

  for (var i = 0; i < rows.length; i++) {
    fragment.appendChild(rows[i]);
  }

  tbody.appendChild(fragment);
}