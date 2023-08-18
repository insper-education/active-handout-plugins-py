
async function updateFilter() {

  exercise_div.innerHTML = "";
  const course_name = "devlife-23-1"
  let student = select_student.value;
  let week_label = select_week.value;
  select_week.value = "";

  let week = week_data[week_label];
  await fetch(`${course_name}/${student}/${week}`).then(async (response) => {
    const data = await response.json();
    showStuff(data);
  });
}

function showStuff(data) {
  let tag_div = document.createElement("div");
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
      plugins: {

        title: {
          display: true,
          text: "Tag distribution"
        },
      },
      responsive: true,
      maintainAspectRatio: false,
    }
  });
  var total = document.createTextNode(`Total: ${data["total"]}`);
  var average = document.createTextNode(`Average points: ${data["average_points"]}\n`);

  exercise_div.appendChild(total);
  exercise_div.appendChild(document.createElement("br"));
  exercise_div.appendChild(average);
  exercise_div.appendChild(document.createElement("br"));

  for (let i = 0; i < data["exercises"].length; i++) {
    let ex = document.createTextNode(`${data["exercises"][i][0]} - ${data["exercises"][i][1]}`)
    exercise_div.appendChild(ex);
    exercise_div.appendChild(document.createElement("br"));

  }
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