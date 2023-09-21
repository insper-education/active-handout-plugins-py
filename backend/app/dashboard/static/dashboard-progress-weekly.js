
async function updateFilter() {
  let student = selectStudent.value;
  let week_label = selectWeek.value;
  let courseClass = selectClass.value;
  let week = weekData[week_label];
  let student_value;
  await fetch(`${activeCourse}/${courseClass}/${student}/${week}`).then(async (response) => {
    const data = await response.json();
    createExercisesTable(data.exercises);
    createChoiceChart(data.choice)
    createTagChart(data);
    createInfo(data);
    student_value = data["total"];

  });

  await fetch(`${activeCourse}/${courseClass}/${week}`).then(async (response) => {
    const data = await response.json();
    createHistogram(data, student_value);
  });


}
function createInfo(data) {
  let dash = document.getElementById("data");
  dash.style.visibility = "visible";

  let name = document.getElementById("name");
  name.innerHTML = selectStudent.value;

  let week = document.getElementById("week");
  week.innerHTML = selectWeek.value;

  let total = document.getElementById("total");
  total.innerHTML = data["total"]

  let avg = document.getElementById("avg");
  avg.innerHTML = Math.round(data["average_points"] * 100) + "%";
}

function createHistogram(data, student_value) {

  if (histChart != null)
    histChart.destroy();

  let keys = Object.keys(data);
  const colors = Array(keys.length).fill("#808080");
  student_value = parseInt(Math.ceil(student_value / 5)) * 5
  let index = keys.indexOf(String(student_value));
  if (index == -1)
    colors[colors.length - 1] = "#0000FF";
  else
    colors[index] = "#0000FF";

  histChart = new Chart("hist", {
    type: "bar",
    data: {
      labels: Object.keys(data),
      datasets: [{
        label: "Histogram",
        data: Object.values(data),
        backgroundColor: colors,
      }]
    },
    options: {
      responsive: false,
      maintainAspectRatio: false,
    }
  });
}

function createTagChart(data) {
  if (tagChart != null)
    tagChart.destroy();

  tagChart = new Chart("chart", {
    type: "pie",
    data: {
      labels: Object.keys(data.tags),
      datasets: [{
        data: Object.values(data.tags)
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    }
  });
}

function createExercisesTable(data) {
  let filteredData = filterCodeExercise(data);

  if (table != null) {
    table.updateSettings({
      data: filteredData
    })
    return;
  }
  let table_div = document.getElementById("table");
  table = new Handsontable(table_div, {
    data: filteredData,
    colHeaders: ["Slug", "Max points", "Submissions"],
    licenseKey: "non-commercial-and-evaluation", // for non-commercial use only
  });
}

function createChoiceChart(data) {
  if (choiceChart != null)
    choiceChart.destroy();
  let labels = Object.keys(data);
  let values = Object.values(data);
  let correct = values.map(item => item.correct)
  let wrong = values.map(item => item.wrong)
  choiceChart = new Chart("another-chart", {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Right",
          data: correct,
        },
        {
          label: "Wrong",
          data: wrong,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          stacked: true,
        },
        y: {
          stacked: true,
        }
      }
    }
  });
}

function filterCodeExercise(data) {
  for (let key in data) {
    if (data[key]["type"] == "choice") {
      delete data[key]
    } else
      delete data[key].type
  }
  return Object.values(data);
}

function getClassSelect() {
  return document.getElementById("select-class");
}

function getCurrentStudents() {
  const classSelect = getClassSelect();
  const selectedClass = courseClasses[classSelect.selectedIndex];
  return selectedClass.students;
}

function updateStudents() {
  clearData();
  let student_datalist = document.getElementById("students");
  student_datalist.innerHTML = "";
  let currentStudents = getCurrentStudents();
  currentStudents.forEach(item => {
    let option = document.createElement("option");
    option.value = item;
    student_datalist.appendChild(option)
  })

}
function clearData() {
  document.getElementById("data").style.visibility = "hidden";
  selectStudent.value = "";
}

var activeCourse;
var selectStudent;
var selectWeek;
var weekData;
var exercise_div;
var tagChart;
var histChart;
var choiceChart;
var table;
var courseClasses;
var selectClass;

document.addEventListener("DOMContentLoaded", function () {

  let activeButton = document.getElementById("weekly");
  selectClass = document.getElementById("select-class");
  courseClasses = selectClass.getAttribute("data-classes");
  activeButton.className += " active";
  activeCourse = document.getElementById("select-course").value;
  selectStudent = document.getElementById("select-student");
  selectWeek = document.getElementById("select-week");
  exercise_div = document.getElementById("exercise-data");
  weekData = selectWeek.getAttribute("data-week");
  weekData = weekData.replace(/'/g, '"');
  courseClasses = courseClasses.replace(/'/g, '"');
  courseClasses = JSON.parse(courseClasses);
  courseClasses.forEach((courseClass) => {
    courseClass.students = new Set(courseClass.students);
  });


  weekData = JSON.parse(weekData);
  selectStudent.onchange = updateFilter;
  selectWeek.onchange = updateFilter;
  selectClass.onchange = updateStudents;

});