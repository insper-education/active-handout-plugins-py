async function getStudentData() {
  clearAll();
  let student = selectStudent.value
  await fetch(`${activeCourse}/${student}`).then(async (response) => {
    const data = await response.json();
    document.getElementById("data").style.visibility = "visible";
    createTagChart(data);
  });
}

function createTagChart(data) {
  if (tagChart != null)
    tagChart.destroy();
  let labels = Object.keys(data);
  let values = Object.values(data);
  let count = values.map(item => item.count)

  tagChart = new Chart("tag-chart", {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          data: count,
        },
      ]
    },
    options: {
      onClick: function handleBarClick(event, activeElements) {
        if (activeElements.length > 0) {
          let index = activeElements[0].index;
          clearAll();
          createTable(data[labels[index]].data);
        }
      },
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: false
        }
      }
    }
  });
}

function createTable(data) {
  tableData = data;
  let keys = Object.keys(data);
  let formatedData = []
  for (let i = 0; i < keys.length; i++) {
    formatedData.push([keys[i], data[keys[i]].length]);
  }

  let tableDiv = document.getElementById("table");
  document.getElementById("table-div").style.visibility = "visible";


  table = new Handsontable(tableDiv, {
    data: formatedData,
    colHeaders: ["Slug", "Submissions"],
    columns: [
      { data: 0 },
      { data: 1 },
    ],
    licenseKey: "non-commercial-and-evaluation"
  });
  table.addHook('afterSelectionByProp', onRowClicked);
}

function onRowClicked(row, prop) {
  let slug = table.getSourceDataAtRow(row)[0];
  clearInfo();
  createAnswerView(slug, tableData[slug]);
}

function createAnswerView(slug, data) {
  let div = document.getElementById("answers");
  div.innerHTML = "";
  createSubmissionSelect(slug, Object.keys(data), data);
  createFileSelect(data);
}

function createSubmissionSelect(slug, submissions, data) {
  let div = document.getElementById("select-submission");
  let name = document.createElement("p");
  name.innerHTML = slug;

  let title = document.createElement("h5");
  title.innerHTML = "Submission";
  div.appendChild(name);
  div.appendChild(title);

  submissionSelect = document.createElement('select');
  submissionSelect.className = 'form-select';
  submissionSelect.onchange = function () {
    createCode(data[submissionSelect.value], fileSelect.value);
  };

  for (const [key, value] of Object.entries(data.reverse())) {
    const option = document.createElement('option');
    option.value = key;
    //turn submission number in two digits minimum (formatting reasons)  1 -> 01 2 -> 02
    let submissionNumber = (data.length - parseInt(key)).toLocaleString('en-US', {
      minimumIntegerDigits: 2,
      useGrouping: false
    });
    let optionText = `#${submissionNumber} ${value.date.slice(5, 7)}/${value.date.slice(8, 10)} - ${value.date.slice(11, 16)}`
    option.textContent = optionText;
    submissionSelect.appendChild(option);
  };

  div.appendChild(submissionSelect);
}

function createFileSelect(data) {
  let div = document.getElementById("select-file");
  div.innerHTML = "";
  let title = document.createElement("h5");
  title.innerHTML = "File";
  div.appendChild(title);
  fileSelect = document.createElement('select');
  fileSelect.id = 'select-file';
  fileSelect.className = 'form-select';

  fileSelect.onchange = function () {
    createCode(data[submissionSelect.value], fileSelect.value);
  };
  for (key in data[0].log.student_input) {
    const option = document.createElement('option');
    option.value = key;
    option.textContent = key;
    fileSelect.appendChild(option);
  }
  div.appendChild(fileSelect);

  //create codeBlock with the default submission and file
  createCode(data[0], fileSelect.value);

}


function createCode(data, fileName) {

  let body = document.getElementById("answers");
  body.innerHTML = "";

  let codeDiv = document.createElement("div");
  let codeSnippet = document.createElement("div");
  codeSnippet.className = "code-snippet";

  let points = document.createElement("h4");
  points.innerHTML = `Points: ${data.points.toFixed(2)}`;
  codeSnippet.appendChild(points);

  let pre = document.createElement("pre");
  let code = document.createElement("code");
  code.className = "language-python";
  code.innerHTML = data.log.student_input[fileName];

  pre.appendChild(code);
  codeSnippet.appendChild(pre);
  codeDiv.appendChild(codeSnippet);
  body.appendChild(codeDiv);
  Prism.highlightElement(code);

}
function clearInfo() {
  document.getElementById("select-submission").innerHTML = "";
  document.getElementById("select-file").innerHTML = "";
  document.getElementById("answers").innerHTML = "";
}

function clearAll() {
  clearInfo();
  document.getElementById("table").innerHTML = "";
  document.getElementById("table-div").style.visibility = "hidden";

}

var activeCourse;
var selectStudent;
var tagChart;
var table;
var tableData;
var submissionSelect;
var fileSelect;
var courseClasses;
var selectClass;

document.addEventListener("DOMContentLoaded", function () {

  document.getElementById("data").style.visibility = "hidden";
  document.getElementById("table-div").style.visibility = "hidden";


  activeCourse = document.getElementById("select-course").value;

  let activeButton = document.getElementById("student");
  activeButton.className += " active";

  selectStudent = document.getElementById("select-student");
  selectStudent.onchange = getStudentData;

  selectClass = document.getElementById("select-class");
  selectClass.onchange = updateStudents;

  courseClasses = selectClass.getAttribute("data-classes");
  courseClasses = courseClasses.replace(/'/g, '"');
  courseClasses = JSON.parse(courseClasses);
  courseClasses.forEach((courseClass) => {
    courseClass.students = new Set(courseClass.students);
  });




});
