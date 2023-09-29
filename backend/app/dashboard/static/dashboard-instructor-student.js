async function getStudentData() {
    console.log("onGetStudentData");
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
                    label: "Right",
                    data: count,
                },
            ]
        },
        options: {
            onClick: function handleBarClick(event, activeElements) {
                if (activeElements.length > 0) {
                  let index = activeElements[0].index;
                  createAnswerView(data[labels[index]].data);
                }
              },
            indexAxis: 'y',
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

function createAnswerView(data){
    let div = document.getElementById("answers");
    for (let i=0; i<Object.keys(data).length; i++){
        div.appendChild(createAccordionItem(data[i], i));
        }
}

function createAccordionItem(data, index) {
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
    button.textContent = data.slug;

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
  
/*
 <div class="accordion-item">
      <h2 class="accordion-header">
        <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
          Accordion Item #1
        </button>
      </h2>
      <div id="collapseOne" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">
        <div class="accordion-body">
          <strong>This is the first item's accordion body.</strong> It is shown by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
        </div>
      </div>
    </div>
*/
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