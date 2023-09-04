
async function updateFilter() {
  let student = selectStudent.value;
  let week_label = selectWeek.value;
  let week = weekData[week_label];
  let student_value;
  await fetch(`${activeCourse}/${student}/${week}`).then(async (response) => {
    const data = await response.json();
    createExercisesTable(data.exercises);
    createTagChart(data);
    createInfo(data);
    student_value = data["total"];

  });

  await fetch(`${activeCourse}/${week}`).then(async (response) => {
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

  if (table != null) {
    table.updateSettings({
      data: data
    })
    return;
  }

  let table_div = document.getElementById("table");
  table = new Handsontable(table_div, {
    data: data,
    licenseKey: "non-commercial-and-evaluation", // for non-commercial use only
  });
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
  let student_datalist = document.getElementById("students");
  student_datalist.innerHTML = "";
  let currentStudents = getCurrentStudents();
  currentStudents.forEach(item => {
    let option = document.createElement("option");
    option.value = item;
    student_datalist.appendChild(option)
  })

}

var activeCourse;
var selectStudent;
var selectWeek;
var weekData;
var exercise_div;
var tagChart;
var histChart;
var table;
var courseClasses;

document.addEventListener("DOMContentLoaded", function () {

  let activeButton = document.getElementById("weekly");
  let selectClass = document.getElementById("select-class");
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