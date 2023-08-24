
async function updateFilter() {
  exercise_div.innerHTML = "";
  const course_name = "devlife-23-1"
  let student = select_student.value;
  let week_label = select_week.value;
  let week = week_data[week_label];

  await fetch(`${course_name}/${week}`).then(async (response) => {
    const data = await response.json();
    showHistogram(data);
  });

  await fetch(`${course_name}/${student}/${week}`).then(async (response) => {
    const data = await response.json();
    showStuff(data);
    showExercisePerTag(data);
    showDashboard(data);

  });
}
function showDashboard(data) {
  let head_div = document.createElement("div")
  let dash = document.getElementById("dashboard-head");
  dash.style.visibility = "visible";

  let name = document.getElementById("name");
  name.innerHTML = select_student.value;

  let week = document.getElementById("week");
  week.innerHTML = select_week.value;

  let total = document.getElementById("total");
  total.innerHTML = data["total"]

  let avg = document.getElementById("avg");
  avg.innerHTML = Math.round(data["average_points"] * 100) + "%";
}

function showHistogram(data) {
  let tag_div = document.createElement("div");
  tag_div.className = "hist";
  exercise_div.appendChild(tag_div);
  let h3 = document.createElement("h3");
  h3.className = "h3";
  tag_div.appendChild(h3);
  h3.innerText = "Exercises per week"
  let tags_chart_canvas = document.createElement("canvas");
  tags_chart_canvas.id = "histChart";
  tag_div.appendChild(tags_chart_canvas);

  let colorsList = [];
  for (let i = 0; i < Object.keys(data).length; i++) {
    colorsList.push(`#${Math.floor(Math.random() * 16777215).toString(16)}`);
  }
  new Chart("histChart", {
    type: "bar",
    data: {
      labels: Object.keys(data),
      datasets: [{
        label: "Histogram",
        data: Object.values(data),
        backgroundColor: colorsList,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    }
  });
}

function showStuff(data) {
  let tag_div = document.createElement("div");
  let h3 = document.createElement("h3");
  h3.className = "h3";
  tag_div.appendChild(h3);
  h3.innerText = "Tag Distribution"
  tag_div.className = "chart"
  exercise_div.appendChild(tag_div)
  let tags_chart_canvas = document.createElement("canvas");
  tags_chart_canvas.id = "tagChart";
  tag_div.appendChild(tags_chart_canvas);
  new Chart("tagChart", {
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

function showExercisePerTag(data) { 
  console.log(data);
}
var select_student;
var select_week;
var week_data;
var exercise_div;

document.addEventListener('DOMContentLoaded', function () {

  select_student = document.getElementById("select-student");
  select_week = document.getElementById("select-week")
  exercise_div = document.getElementById("exercise-data");
  week_data = select_week.getAttribute("data-week")
  week_data = week_data.replace(/'/g, '"');

  week_data = JSON.parse(week_data);
  select_student.onchange = updateFilter;
  select_week.onchange = updateFilter;

});