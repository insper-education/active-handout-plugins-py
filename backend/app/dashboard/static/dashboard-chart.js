var last_ex = null;

function generateChoice(ex) {
    if (last_ex != null) {
        const element = document.getElementById(`item-${last_ex.name}`);
        element.remove();
    }

    ex = ex.replace(/'/g, '"');
    var exercise = JSON.parse(ex);

    if (exercise.telemetry.x.length == 0) {
        last_ex = null;
        return;
    }
    last_ex = exercise;

    var item_div = document.createElement("div");
    item_div.id = "item-" + exercise.name;
    item_div.className = "item";


    var canvas = document.createElement("canvas");
    canvas.id = `canvas-${exercise.name}-chart`;

    document.getElementById(exercise.name).appendChild(item_div);
    item_div.appendChild(canvas);

    var barColors = [
        "#b91d47",
        "#00aba9",
        "#2b5797",
        "#e8c3b9",
        "#1e7145"
    ];
    generateChart(exercise.name, exercise.telemetry.x, exercise.telemetry.y, "pie", barColors);
}


function getWrongLines(answer, correct) {
    var answer_lines = answer.split("\n");
    var correct_split = [];
    var wrong_lines = [];

    if (correct.length == 0)
        return [];
    for (var i = 0; i < correct.length; i++) {
        correct_split.push(correct[i].split("\n"));
    }
    for (var i = 0; i < answer_lines.length; i++) {
        isCorrect = false;
        for (var j=0; j<correct_split.length; j++){
            if (correct_split[j][i] == answer_lines[i])
                isCorrect = true;
        }
        if (!isCorrect)
            wrong_lines.push(i + 1);
    }
    return wrong_lines;
}

function generateParson(ex) {

    if (last_ex != null) {
        const element = document.getElementById(`item-${last_ex.name}`);
        element.remove();
    }

    ex = ex.replace(/'/g, '"');
    ex = ex.replace(/\\\\/g, '\\');

    var exercise = JSON.parse(ex);
    if (exercise.telemetry.x.length == 0) {
        last_ex = null;
        return;
    }
    last_ex = exercise;
    var item_div = document.createElement("div");
    item_div.id = "item-" + exercise.name;
    item_div.className = "item";

    var canvas = document.createElement("canvas");
    canvas.id = `canvas-${exercise.name}-chart`;

    answer_div = document.createElement("div");
    answer_div.className = "parson-answers";

    document.getElementById(exercise.name).appendChild(item_div);
    item_div.appendChild(canvas);
    item_div.appendChild(answer_div);

    var colors = [];
    var x_values = [];

    for (answer in exercise.telemetry.y) {

        var color = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
        colors.push(color);
        x_values.push(exercise.telemetry.x[answer]);

        var lines = getWrongLines(exercise.telemetry.y[answer], exercise.telemetry.correct);
        var code_div = document.createElement("div");
        var pre = document.createElement("pre");
        var code = document.createElement("code");

        code.className = "language-python";
        code.innerHTML = exercise.telemetry.y[answer];
        pre.setAttribute("data-line", lines.join(","));
        code_div.style.backgroundColor = color;
        code_div.className = "parson-code";

        answer_div.appendChild(code_div);
        code_div.appendChild(pre);
        pre.appendChild(code);


        Prism.highlightElement(code);

    }
    labels = [];
    //create label list from A until length of x_values in one line
    for (var i = 0; i < x_values.length; i++) {
        labels.push(String.fromCharCode(65 + i));
    }

    generateChart(exercise.name, x_values, labels, "bar", colors);

}

function generateChart(name, data, labels, type, colors) {

    Chart.defaults.global.legend.display = false;
    if (type == "pie")
        scales = {};
    else
        scales = {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        };

    new Chart(`canvas-${name}-chart`, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                backgroundColor: colors,
                data: data
            }]
        },
        options: {
            title: {
                display: true,
                text: name
            },
            responsive: false,
            maintainAspectRatio: false,
            scales: scales,

        }
    });

}