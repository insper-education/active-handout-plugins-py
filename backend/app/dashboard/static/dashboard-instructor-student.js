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
    createSubmissionSelect(slug, Object.keys(data), data);
    createFileSelect(data)
    //for (let i = 0; i < Object.keys(data).length; i++) {
    //    div.appendChild(createAccordionItem(slug, data[i], i));
    //}
}

function createSubmissionSelect(slug, submissions, data) {
    console.log(data);
    let div = document.getElementById("select-submission");

    // Create the select element
    submissionSelect = document.createElement('select');
    submissionSelect.className = 'form-select';
    submissionSelect.onchange = function () {
        createAccordionItem(fileSelect.value, data[submissionSelect.value], 0, fileSelect.value);
    };

    // Iterate through the courseList and create option elements
    for (const [key, value] of Object.entries(data)) {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = `${value.date.slice(5,10)}  ${value.date.slice(11,16)}`;
        submissionSelect.appendChild(option);
    };

    // Append the select element to the document or another parent element
    div.appendChild(submissionSelect);
}

function createFileSelect(data) {
    let div = document.getElementById("select-file");
    div.innerHTML = "";

    // Create the select element
    fileSelect = document.createElement('select');
    fileSelect.id = 'select-file';
    fileSelect.className = 'form-select';
    console.log(data);
    console.log("udhsbusdsd");
    fileSelect.onchange = function () {
        createAccordionItem(fileSelect.value, data[submissionSelect.value], 0, fileSelect.value);
        //div.appendChild(createAccordionItem(slug, data[select.value], 0));
    };

    // Iterate through the courseList and create option elements
    console.log(data, "dataaaaaaaaaaaaa");
    if (data[0].log.student_input) {
        for (key in data[0].log.student_input){
            console.log(key);
            const option = document.createElement('option');
            option.value = key;
            option.textContent = key;
            fileSelect.appendChild(option);
        }
        div.appendChild(fileSelect);

    }
    else {
        //document.getElementById("answers").appendChild(createCode(data.log, "uwu"));
    }
    createAccordionItem(fileSelect.value, data[0], 0, fileSelect.value);

    // Append the select element to the document or another parent element
}

function createAccordionItem(slug, data, index, file) {
    document.getElementById("answers").innerHTML= "";

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
    collapse.classList.add("accordion-collapse", "collapse", "show");
    collapse.setAttribute("id", `collapse-${index}`);
    const body = document.createElement("div");
    body.classList.add("accordion-body");
    console.log("FIle  " + file)
    body.appendChild(createCode(data, file));

    collapse.appendChild(body);
    header.appendChild(button);
    item.appendChild(header);
    item.appendChild(collapse);

    document.getElementById("answers").appendChild(item);

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
    console.log("onCreateCOde", data, fileName);
    let codeDiv = document.createElement("div");
    let codeSnippet = document.createElement("div");
    codeSnippet.className = "code-snippet";
    let fileNameDiv = document.createElement("div");
    fileNameDiv.className = "file-name";
    fileNameDiv.innerHTML = fileName;

    let pre = document.createElement("pre");
    let code = document.createElement("code");
    code.className = "language-python";
    code.innerHTML = data.log.student_input[fileName];
    pre.appendChild(code);
    codeSnippet.appendChild(pre);
    Prism.highlightElement(code);
    codeDiv.appendChild(fileNameDiv);
    codeDiv.appendChild(codeSnippet);
    console.log("aaa" + codeDiv);
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
var submissionSelect;
var fileSelect;
document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("data").style.visibility = "hidden";

    activeCourse = document.getElementById("select-course").value;

    let activeButton = document.getElementById("student");
    activeButton.className += " active";

    selectStudent = document.getElementById("select-student");
    selectStudent.onchange = getStudentData;


});