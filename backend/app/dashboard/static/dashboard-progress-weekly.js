function getPastSundayDate(weeksAgo) {
  const currentDate = new Date();
  const currentDay = currentDate.getDay(); // Sunday is 0, Monday is 1, ..., Saturday is 6
  const daysUntilLastSunday = (currentDay === 0) ? 7 : currentDay;

  const daysAgo = weeksAgo * 7 + daysUntilLastSunday;

  return new Date(currentDate.getTime() - (daysAgo * 24 * 60 * 60 * 1000));
}


async function updateFilter() {
  const course_name = "devlife-23-1"
  var student = select_student.value;
  var week = select_week.value;

  await fetch(`${course_name}/${student}/${week}`).then(async (response) => {
    const data = await response.json();
    showStuff(data);
  });
}

function showStuff(data) {

  console.log(data);
  var div = document.getElementById("exercise-data");
  div.innerHTML = "";

  var total = document.createTextNode(`Total: ${data["total"]}`);
  var average = document.createTextNode(`Average points: ${data["average_points"]}\n`);

  div.appendChild(total);
  div.appendChild(document.createElement("br"));
  div.appendChild(average);
  div.appendChild(document.createElement("br"));



  Object.keys(data["tags"]).forEach(key => {
    let tag = document.createTextNode(`${key} - ${data["tags"][key]}\n`)
    div.appendChild(tag);
    div.appendChild(document.createElement("br"));
  })
  for (let i =0; i<data["exercises"].length;i++){
    let ex = document.createTextNode(`${data["exercises"][i][0]} - ${data["exercises"][i][1]}`)
    div.appendChild(ex);
    div.appendChild(document.createElement("br"));

  }
}




var select_student;
var select_week;

document.addEventListener('DOMContentLoaded', function () {
  select_student = document.getElementById("select-student");
  select_week = document.getElementById("select-week")
  select_student.onchange = updateFilter;
  select_week.onchange = updateFilter;

});