
async function updateFilter() {
  let student = select_student.value;
  let week_label = select_week.value;
  let week = week_data[week_label];
  let student_value;
  await fetch(`${activeCourse}/${student}/${week}`).then(async (response) => {
    const data = await response.json();
    createExercisesTable(data.exercises);
    createTagChart(data);
    createInfo(data);
    student_value = data['total'];

  });

  await fetch(`${activeCourse}/${week}`).then(async (response) => {
    const data = await response.json();
    createHistogram(data, student_value);
  });


}
function createInfo(data) {
  let dash = document.getElementById('data');
  dash.style.visibility = 'visible';

  let name = document.getElementById('name');
  name.innerHTML = select_student.value;

  let week = document.getElementById('week');
  week.innerHTML = select_week.value;

  let total = document.getElementById('total');
  total.innerHTML = data['total']

  let avg = document.getElementById('avg');
  avg.innerHTML = Math.round(data['average_points'] * 100) + '%';
}

function createHistogram(data, student_value) {

  if (histChart != null)
    histChart.destroy();

  let keys = Object.keys(data);
  const colors = Array(keys.length).fill('#808080');
  student_value = parseInt(Math.ceil(student_value / 5)) * 5
  let index = keys.indexOf(String(student_value));
  if (index == -1)
    colors[colors.length - 1] = '#0000FF';
  else
    colors[index] = '#0000FF';

  histChart = new Chart('hist', {
    type: 'bar',
    data: {
      labels: Object.keys(data),
      datasets: [{
        label: 'Histogram',
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

  tagChart = new Chart('chart', {
    type: 'pie',
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

  let table_div = document.getElementById('table');
  table = new Handsontable(table_div, {
    data: data,
    licenseKey: 'non-commercial-and-evaluation', // for non-commercial use only
  });
}
var activeCourse;
var select_student;
var select_week;
var week_data;
var exercise_div;
var tagChart;
var histChart;
var table;

document.addEventListener('DOMContentLoaded', function () {

  let active_button = document.getElementById('weekly');
  active_button.className += ' active';
  activeCourse = document.getElementById('select-course').value;
  select_student = document.getElementById('select-student');
  select_week = document.getElementById('select-week');
  exercise_div = document.getElementById('exercise-data');
  week_data = select_week.getAttribute('data-week');
  week_data = week_data.replace(/'/g, '"');

  week_data = JSON.parse(week_data);
  select_student.onchange = updateFilter;
  select_week.onchange = updateFilter;

});