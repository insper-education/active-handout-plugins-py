async function getStudentData() {
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
                    label: "Total Exercises by Tag",
                    data: count,
                },
            ]
        },
        options: {
            onClick: function handleBarClick(event, activeElements) {
                if (activeElements.length > 0) {
                  let index = activeElements[0].index;
                  createTable(data[labels[index]].data);
                  //createAnswerView(data[labels[index]].data);
                }
              },
            indexAxis: "y",
            responsive: false,
            maintainAspectRatio: true,
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

function createAnswerView(slug, data){
    let div = document.getElementById("answers");
    for (let i=0; i<Object.keys(data).length; i++){
        div.appendChild(createAccordionItem(slug, data[i], i));
        }
}

function createTable(data){
    let keys = Object.keys(data);
    let formatedData = []
    for (let i=0; i<keys.length; i++){
        formatedData.push([keys[i], data[keys[i]].length]);
    }
    let table = document.getElementById("table");
    const hot = new Handsontable(table, {
        data: formatedData,
        colHeaders: ["Slug", "Submissions"],
        columns: [
            {data: 0},
            {data: 1},
        ],
        licenseKey: "non-commercial-and-evaluation"
      });
      hot.addHook('afterSelectionByProp', (row, prop) => {
        let slug = hot.getSourceDataAtRow(row)[0];
        createAnswerView(slug, data[slug]);
      });
}

function createAccordionItem(slug, data, index) {
    const item = document.createElement("div");
    item.classList.add("accordion-item");

    const header = document.createElement("h2");
    header.classList.add("accordion-header");

    const button = document.createElement("button");
    button.classList.add("accordion-button");
    button.setAttribute("type", "button");
    button.setAttribute("data-bs-toggle", "collapse");
    button.setAttribute("data-bs-target", `#collapse-${index}`);
    button.setAttribute("aria-expanded", "false"); // Change this to "true" for the first item
    button.setAttribute("aria-controls", `collapse-${index}`);
    button.textContent = slug + " - Submissão #" + (index+1);

    const collapse = document.createElement("div");
    collapse.classList.add("accordion-collapse", "collapse");
    collapse.setAttribute("id", `collapse-${index}`);

    const body = document.createElement("div");
    body.classList.add("accordion-body");
    if (data.log.code)
        body.innerHTML = data.log.code ;
    else if (data.log.student_input)
        body.innerHTML = data.log.student_input["solution.py"];
    else
        body.innerHTML = data.log;

    collapse.appendChild(body);
    header.appendChild(button);
    item.appendChild(header);
    item.appendChild(collapse);

    return item;
  }

var activeCourse;
var selectStudent;

var tagChart;
document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("data").style.visibility = "hidden";

    activeCourse = document.getElementById("select-course").value;

    let activeButton = document.getElementById("student");
    activeButton.className += " active";

    selectStudent = document.getElementById("select-student");
    selectStudent.onchange = getStudentData;


});