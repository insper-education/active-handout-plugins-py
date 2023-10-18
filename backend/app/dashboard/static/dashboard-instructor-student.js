async function getStudentData() {
    clearAll();
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
                    clearAll();
                    createTable(data[labels[index]].data);
                }
            },
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
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

    let tableDiv = document.getElementById("table");
    document.getElementById("table-div").style.visibility = "visible";


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
    clearInfo();
    createAnswerView(slug, tableData[slug]);
}

function createAnswerView(slug, data) {
    let div = document.getElementById("answers");
    div.innerHTML = "";
    createSubmissionSelect(slug, Object.keys(data), data);
    createFileSelect(data)
}

function createSubmissionSelect(slug, submissions, data) {
    let div = document.getElementById("select-submission");
    let name = document.createElement("p");
    name.innerHTML = slug;

    let title = document.createElement("h5");
    title.innerHTML = "Submission";
    div.appendChild(name);
    div.appendChild(title);

    // Create the select element
    submissionSelect = document.createElement('select');
    submissionSelect.className = 'form-select';
    submissionSelect.onchange = function () {
        createAccordionItem(fileSelect.value, data[submissionSelect.value], 0, fileSelect.value);
    };

    // Iterate through the courseList and create option elements
    for (const [key, value] of Object.entries(data.reverse())) {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = `#${(data.length - parseInt(key)).toLocaleString('en-US',{    minimumIntegerDigits: 2,
            useGrouping: false})} ${value.date.slice(5, 7)}/${value.date.slice(8, 10)} - ${value.date.slice(11, 16)}`;
        submissionSelect.appendChild(option);
    };

    // Append the select element to the document or another parent element
    div.appendChild(submissionSelect);
}

function createFileSelect(data) {
    let div = document.getElementById("select-file");
    div.innerHTML = "";
    let title = document.createElement("h5");
    title.innerHTML = "File";
    div.appendChild(title);
    // Create the select element
    fileSelect = document.createElement('select');
    fileSelect.id = 'select-file';
    fileSelect.className = 'form-select';
    console.log(data);
    fileSelect.onchange = function () {
        createAccordionItem(fileSelect.value, data[submissionSelect.value], 0, fileSelect.value);
    };

    if (data[0].log.student_input) {
        for (key in data[0].log.student_input) {
            console.log(key);
            const option = document.createElement('option');
            option.value = key;
            option.textContent = key;
            fileSelect.appendChild(option);
        }
        div.appendChild(fileSelect);

    }
    createAccordionItem(fileSelect.value, data[0], 0, fileSelect.value);

}

function createAccordionItem(slug, data, index, file) {
    console.log(data);
    document.getElementById("answers").innerHTML = "";
    let body = document.getElementById("answers");
    body.appendChild(createCode(data, file));

}

function createCode(data, fileName) {
    let codeDiv = document.createElement("div");
    let codeSnippet = document.createElement("div");
    codeSnippet.className = "code-snippet";

    let points = document.createElement("h4");
    points.innerHTML = `Points: ${data.points.toFixed(2)}`;

    codeSnippet.appendChild(points);
    let pre = document.createElement("pre");
    let code = document.createElement("code");
    code.className = "language-python";
    code.innerHTML = data.log.student_input[fileName];
    pre.appendChild(code);
    codeSnippet.appendChild(pre);
    Prism.highlightElement(code);
    codeDiv.appendChild(codeSnippet);
    return codeDiv;

}
function clearInfo() {
    document.getElementById("select-submission").innerHTML = "";
    document.getElementById("select-file").innerHTML = "";
    document.getElementById("answers").innerHTML = "";
}

function clearAll() {
    clearInfo();
    document.getElementById("table").innerHTML = "";
    document.getElementById("table-div").style.visibility = "hidden";

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
    document.getElementById("table-div").style.visibility = "hidden";


    activeCourse = document.getElementById("select-course").value;

    let activeButton = document.getElementById("student");
    activeButton.className += " active";

    selectStudent = document.getElementById("select-student");
    selectStudent.onchange = getStudentData;


});