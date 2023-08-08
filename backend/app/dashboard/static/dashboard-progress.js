
function createHandsontable(data, columns_list) {

  var container = document.getElementById('table');
  Handsontable.renderers.registerRenderer('colorFormattingRenderer', function (
    instance,
    td,
    row,
    col,
    prop,
    value,
    cellProperties
  ) {
    cellProperties.editor = false;
    Handsontable.renderers.TextRenderer.apply(this, arguments);
    td.style.color = 'black';
    var cell_value = parseFloat(value);
    if (cell_value == 1) {
      td.style.background = 'green';
    }
    else if (cell_value == 0) {
      td.style.background = 'red';
    }
    else if ((cell_value > 0) && (cell_value < 1)) {
      td.style.background = '#ffae00'
    }
  });

  hot = new Handsontable(container, {
    data: data,
    colHeaders: columns_list,
    columns: function (column) {
      columnMeta = {};
      columnMeta.data = columns_list[column]
      return columnMeta;
    },
    colWidths: [100].concat(Array(columns_list.length - 1).fill(30)),
    fixedColumnsStart: 1,
    cells: function (row, col, prop) {
      var cellProperties = {};
      cellProperties.renderer = 'colorFormattingRenderer';
      return cellProperties;
    },
    licenseKey: 'non-commercial-and-evaluation', // for non-commercial use only

  });
}

function updateHandsontable(data, columns_list) {

  hot.updateSettings({
    data: data,
    colHeaders: columns_list,
    columns: function (column) {
      columnMeta = {};
      columnMeta.data = columns_list[column]
      return columnMeta;
    }, colWidths: [100].concat(Array(columns_list.length - 1).fill(30)),
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

  var filteredColumns = ["Name"]
  exerciseList = []
  if (tags.size == 0) {
    updateHandsontable(clonedData, clonedColumns);
    return;
  }
  tags.forEach(tag => {
    exerciseList = exerciseList.concat(tagsObj[tag]);
  });
  for (var i = 0; i < exerciseList.length; i++) {
    var column_index = clonedColumns.indexOf(exerciseList[i]);
    if (column_index != -1)
      filteredColumns = filteredColumns.concat(clonedColumns.splice(column_index,1));
  }

  updateHandsontable(clonedData, filteredColumns);
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


  var select = document.getElementById("select-tag")
  select.onchange = updateFilter;

  tableData = structuredClone(data);

  createHandsontable(tableData, columns);
});