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
                    clearCodeBlock();
                    createTable(data[labels[index]].data);
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

function createTable(data) {
    tableData = data;
    let keys = Object.keys(data);
    let formatedData = []
    for (let i = 0; i < keys.length; i++) {
        formatedData.push([keys[i], data[keys[i]].length]);
    }
    if (table) {
        table.updateSettings({ data: formatedData });
        return;
    }
    let tableDiv = document.getElementById("table");
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
    clearCodeBlock();
    createAnswerView(slug, tableData[slug]);
}

function createAnswerView(slug, data) {
    let div = document.getElementById("answers");
    div.innerHTML = "";
    for (let i = 0; i < Object.keys(data).length; i++) {
        div.appendChild(createAccordionItem(slug, data[i], i));
    }
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
    button.textContent = slug + " - Submissão #" + (index + 1);

    const collapse = document.createElement("div");
    collapse.classList.add("accordion-collapse", "collapse");
    collapse.setAttribute("id", `collapse-${index}`);

    const body = document.createElement("div");
    body.classList.add("accordion-body");
    body.appendChild(createCodeBlock(data.log))

    collapse.appendChild(body);
    header.appendChild(button);
    item.appendChild(header);
    item.appendChild(collapse);

    return item;
}

function createCodeBlock(data) {

    if (data.code) {
        return createCode(data.code, "");

    }
    else if (data.student_input) {
        let codeContainer = document.createElement("div");

        Object.keys(data.student_input).forEach(key => {
            codeContainer.appendChild(createCode(data.student_input[key], key),);
        });
        return codeContainer;

    }


}
function createCode(data, fileName) {
    let codeDiv = document.createElement("div");
    let codeSnippet = document.createElement("div");
    codeSnippet.className = "code-snippet";
    let fileNameDiv = document.createElement("div");
    fileNameDiv.className = "file-name";
    fileNameDiv.innerHTML = fileName;

    let pre = document.createElement("pre");
    let code = document.createElement("code");
    code.className = "language-python";
    code.innerHTML = data;
    pre.appendChild(code);
    codeSnippet.appendChild(pre);
    Prism.highlightElement(code);
    codeDiv.appendChild(fileNameDiv);
    codeDiv.appendChild(codeSnippet);
    return codeDiv;

}
function clearCodeBlock() {
    document.getElementById("answers").innerHTML = "";
}
var activeCourse;
var selectStudent;
var tagChart;
var table;
var tableData;
document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("data").style.visibility = "hidden";

    activeCourse = document.getElementById("select-course").value;

    let activeButton = document.getElementById("student");
    activeButton.className += " active";

    selectStudent = document.getElementById("select-student");
    selectStudent.onchange = getStudentData;


});