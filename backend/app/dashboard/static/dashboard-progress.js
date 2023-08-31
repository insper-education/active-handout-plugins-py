function createHandsontable(data, columns_list) {
  data = filterStudentsInClass(data);

  const container = document.getElementById("table");
  let dataSchema = getDataSchema(columns_list);
  Handsontable.renderers.registerRenderer(
    "colorFormattingRenderer",
    function (instance, td, row, col, prop, value, cellProperties) {
      cellProperties.editor = false;
      Handsontable.renderers.TextRenderer.apply(this, arguments);
      td.style.color = "black";
      const cell_value = parseFloat(value);
      if (cell_value == 1) {
        td.style.background = "green";
      } else if (cell_value == 0) {
        td.style.background = "red";
      } else if (cell_value > 0 && cell_value < 1) {
        td.style.background = "#ffae00";
      }
    }
  );

  hot = new Handsontable(container, {
    data: data,
    dataSchema: dataSchema,
    colHeaders: columns_list,
    columns: function (column) {
      columnMeta = {};
      columnMeta.data = columns_list[column];
      return columnMeta;
    },
    colWidths: [100].concat(Array(columns_list.length - 1).fill(30)),
    fixedColumnsStart: 1,
    cells: function (row, col, prop) {
      const cellProperties = {};
      cellProperties.renderer = "colorFormattingRenderer";
      return cellProperties;
    },
    licenseKey: "non-commercial-and-evaluation", // for non-commercial use only
  });
}

function updateHandsontable(data, columns_list) {
  console.log(data)
  data = filterStudentsInClass(data);
  
  ret = generateMatrix(data, columns_list)
  usernames = ret[0]
  zvals = ret[1]
  data_h[0]['x'] = columns_list.slice(1);
  data_h[0]['y'] = usernames;
  data_h[0]['z'] = zvals;
  Plotly.redraw('chart');

  ret = generateMatrix(data, columns_list)
  zvals = ret[1]
  data_h[0]['x'] = columns_list.slice(1);
  data_h[0]['z'] = zvals;
  Plotly.redraw('chart');

  let dataSchema = getDataSchema(columns_list);
  hot.updateSettings({
    data: data,
    dataSchema: dataSchema,
    colHeaders: columns_list,
    columns: function (column) {
      columnMeta = {};
      columnMeta.data = columns_list[column];
      return columnMeta;
    },
    colWidths: [100].concat(Array(columns_list.length - 1).fill(30)),
  });
}

function getDataSchema(columns_list) {
  var dataSchema =  { name: null };
  for (var i=0;i<columns_list.length;i++){
    dataSchema[columns_list[i]] = null
  }
  return dataSchema;

}

function getTagSelect() {
  return document.getElementById("select-tag");
}

function getClassSelect() {
  return document.getElementById("select-class");
}

function getCurrentStudents() {
  const classSelect = getClassSelect();
  const selectedClass = courseClasses[classSelect.selectedIndex];
  return selectedClass.students;
}

function filterStudentsInClass(data) {
  const currentStudents = getCurrentStudents();
  return data.filter((row) => currentStudents.has(row.Name));
}

function updateFilter() {
  const select = getTagSelect();
  const newValue = select.value;
  select.value = "";

  if (!Object.keys(tagsObj).includes(newValue)) return;
  tags.add(newValue);
  generateTagView();
  updateTableContent();
}

function updateTableContent() {
  console.log("updating table?...")
  const clonedData = structuredClone(data);
  const clonedColumns = structuredClone(columns);
  console.log("Cloned", clonedData);
  let filteredColumns = ["Name"];
  exerciseList = [];
  if (tags.size == 0) {
    updateHandsontable(clonedData, clonedColumns);
    return;
  }
  tags.forEach((tag) => {
    exerciseList = exerciseList.concat(tagsObj[tag]);
  });
  for (var i = 0; i < exerciseList.length; i++) {
    const column_index = clonedColumns.indexOf(exerciseList[i]);
    if (column_index != -1)
      filteredColumns = filteredColumns.concat(
        clonedColumns.splice(column_index, 1)
      );
  }
  console.log(clonedData);

  updateHandsontable(clonedData, filteredColumns);
}

function removeTag(ev) {
  tags.delete(ev.target.id);
  generateTagView();
  updateTableContent();
}

function generateTagView() {
  const tagsDiv = document.getElementById("tags-list");
  tagsDiv.innerHTML = "";
  tags.forEach((element) => {
    const tagDiv = document.createElement("div");
    tagDiv.className = "tag";
    const remove = document.createElement("button");
    remove.className = "btn btn-secondary";
    remove.onclick = removeTag;
    remove.innerText = element;
    remove.id = element;
    tagDiv.appendChild(remove);
    tagsDiv.appendChild(tagDiv);
  });
}

function generateMatrix(tableData, columns){
  nulls = new Array(columns.length-1).fill(null)
  zvals = []
  usernames = []
  tableData.forEach(row => {
    studentvals = [...nulls]
    Object.entries(row).forEach((val) => {
      if (val[0] == "Name") {
        usernames.push(val[1])
      }
      else{
        idx = columns.indexOf(val[0])-1
        if (idx >= 0){
          studentvals[idx] = val[1]
        }
      }  
    });
    zvals.push(studentvals)
  });
  return [usernames.reverse(), zvals.reverse()]
}

var tags = new Set();
var table;
var columns;
var data;
var courseClasses;
var tags;
var hot;

document.addEventListener("DOMContentLoaded", function () {
  table = document.getElementById("table");
  columns = table.getAttribute("data-columns");
  data = table.getAttribute("data-data");
  tagsObj = table.getAttribute("data-tags");
  courseClasses = table.getAttribute("data-classes");

  //cleaning
  data = data.replace(/'/g, '"');
  columns = columns.replace(/'/g, '"');
  courseClasses = courseClasses.replace(/'/g, '"');
  tagsObj = tagsObj.replace(/'/g, '"').replace(/(\w+):/g, '"$1":');

  data = JSON.parse(data);
  columns = JSON.parse(columns);
  courseClasses = JSON.parse(courseClasses);
  tagsObj = JSON.parse(tagsObj);

  courseClasses.forEach((courseClass) => {
    courseClass.students = new Set(courseClass.students);
  });

  const tagSelect = getTagSelect();
  tagSelect.onchange = updateFilter;

  const classSelect = getClassSelect();
  classSelect.onchange = updateTableContent;
  tableData = structuredClone(data);

  createHandsontable(tableData, columns);

  data = filterStudentsInClass(tableData);
  ret = generateMatrix(data, columns)
  usernames = ret[0]
  zvals = ret[1]
  data_h = [
    {
      x: columns.slice(1),
      y: usernames,
      z: zvals,
      type: 'heatmap',
      hovertemplate : 'Exercício: %{x}<br> Aluno: %{y}<br> Nota: %{z}<extra></extra>',
      colorscale:[[0.0, "red"], [0.1, "red"],
                  [0.1, "orange"], [1, "orange"],
                  [1, "green"],  [1.00, "green"]],
      showscale:false,
      xgap:0.5,
      ygap:0.5,
    }
  ];

  var layout = {
    margin: {
      t: 50,
      r: 50,
      b: 0,
      l: 150
    },
    xaxis: {showticklabels: false, ticks: "", side:"top"},
    showlegend: false,
    height: Math.max(400, usernames.length * 25),
    autosize: true
  };

  Plotly.newPlot('chart', data_h, layout);
});

function toggleVisibility() {
  var table = document.getElementById("table");
  var chart = document.getElementById("chart");
  if (table.style.display === "none") {
    table.style.display = "";
    chart.style.display = "none";
  } else {
    table.style.display = "none";
    chart.style.display = "";
    document.querySelector('[data-title="Autoscale"]').click()
  }
} 