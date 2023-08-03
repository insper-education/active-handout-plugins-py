
function createHandsontable(data, columns, colHeaders) {

  var container = document.getElementById('table');


  var dataSchema = [];
  columns.forEach(col => {
    dataSchema.push({ data: col });
  });
  Handsontable.renderers.registerRenderer('colorFormattingRenderer', function (
    instance,
    td,
    row,
    col,
    prop,
    value,
    cellProperties
  ) {
    Handsontable.renderers.TextRenderer.apply(this, arguments);
    td.style.color = 'black';
    if (parseFloat(value) == 1) {
      td.style.background = 'green';
    }
    else if (parseFloat(value) == 0) {
      td.style.background = 'red';
    }
  });

  hot = new Handsontable(container, {
    data: data,
    colHeaders: colHeaders,
    columns: columns,
    colWidths: [100].concat(Array(columns.length - 1).fill(30)),
    fixedColumnsStart: 1,
    cells: function (row, col, prop) {
      var cellProperties = {};
      cellProperties.renderer = 'colorFormattingRenderer';
      return cellProperties;
    },
    licenseKey: 'non-commercial-and-evaluation', // for non-commercial use only

  });

}

function prepareColumns(columns) {
  var colHeaders = ["Name"]
  var colObjList = [{ data: "Name" }]
  for (var i = 0; i < columns.length; i++) {
    var colObj = {
      data: columns[i],
    }
    colHeaders.push(columns[i])
    colObjList.push(colObj);
  }
  return [colObjList, colHeaders];
}
function updateHandsontable(data, columns) {

  var [colObjList, colHeaders] = prepareColumns(columns);

  hot.updateSettings({
    data: data,
    colHeaders: colHeaders,
    columns: colObjList,
    colWidths: [100].concat(Array(columns.length - 1).fill(30)),
  });


}

function updateFilter() {
  var newValue = document.getElementById("select-tag").value;
  if (!Object.keys(tagsObj).includes(newValue))
    return;
  tags.add(newValue);
  generateTagView();
  updateTableContent();


}

function updateTableContent() {

  var clonedData = structuredClone(data);
  var clonedColumns = structuredClone(columns);

  var filteredColumns = []
  exerciseList = []
  if (tags.size == 0) {
    updateHandsontable(clonedData, clonedColumns);
    return;
  }
  tags.forEach(tag => {
    exerciseList = exerciseList.concat(tagsObj[tag][0]);
  });
  for (var i = 0; i < exerciseList.length; i++) {
    filteredColumns = filteredColumns.concat(clonedColumns.splice(clonedColumns.indexOf(exerciseList[i]), 1));
  }

  var [colObjList, colHeaders] = prepareColumns(filteredColumns);

  hot.updateSettings({
    data: clonedData,
    colHeaders: colHeaders,
    columns: colObjList,
    colWidths: [100].concat(Array(filteredColumns.length - 1).fill(30)),
    fixedColumnsStart: 1,
    cells: function (row, col, prop) {
      var cellProperties = {};
      cellProperties.renderer = 'colorFormattingRenderer';
      return cellProperties;
    },
    licenseKey: 'non-commercial-and-evaluation', // for non-commercial use only

  });

}
function removeTag(ev) {
  tags.delete(ev.target.id);
  generateTagView();
  updateTableContent()
}

function generateTagView() {
  var tagsDiv = document.getElementById("tags-list");
  tagsDiv.innerHTML = "";
  tags.forEach(element => {
    var tagDiv = document.createElement("div");
    tagDiv.className = "tag";
    var remove = document.createElement("button")
    remove.className = "btn btn-secondary"
    remove.onclick = removeTag;
    remove.innerText = element
    remove.id = element;
    tagDiv.appendChild(remove);
    tagsDiv.appendChild(tagDiv);

  });
}


var tags = new Set();
var table;
var columns;
var data;
var tags;

var hot;




document.addEventListener('DOMContentLoaded', function () {
  
  table = document.getElementById('table');
  columns = table.getAttribute('data-columns');
  data = table.getAttribute('data-data');
  tagsObj = table.getAttribute('data-tags')

  //cleaning
  data = data.replace(/'/g, '"');
  columns = columns.replace(/'/g, '"');
  tagsObj = tagsObj.replace(/'/g, '"').replace(/(\w+):/g, '"$1":');



  data = JSON.parse(data);
  columns = JSON.parse(columns)
  tagsObj = JSON.parse(tagsObj);

  var [colObjList, colHeaders] = prepareColumns(columns);

  var select = document.getElementById("select-tag")
  select.onchange = updateFilter;

  tableData = structuredClone(data);

  createHandsontable(tableData, colObjList, colHeaders); // Call your function here
});