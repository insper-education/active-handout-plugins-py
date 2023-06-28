function convertToQuote(text) {
    const controlCharacters = {
        "&#x27;": "'",
        "&quot;": '"',
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&#x60;": "`",
        "&#x2F;": "/",
        "&#x5C;": "\\",
        "&#x7B;": "{",
        "&#x7D;": "}",
        "&#x5B;": "[",
        "&#x5D;": "]",
        "&#x23;": "#",
        "&#x3A;": ":",
        "&#x3D;": "=",
        "&#x2D;": "-",
        "&#x28;": "(",
        "&#x29;": ")",
        "&#x5F;": "_",
        "&#x3B;": ";",
        "&#x2C;": ",",
        "&#x2B;": "+",
        "&#x21;": "!",
        "&#x24;": "$",
        "&#x25;": "%",
        "&#x40;": "@",
        "&#x7E;": "~",
        "&#x5E;": "^",
        "&#x3F;": "?",
        "&#x7C;": "|",
        "&#x2A;": "*",
        "&#x2E;": ".",
        "&#x0A;": "\n",
        "&#x0D;": "\r",
        "&#x09;": "\t",
        "&#x0B;": "\v",
        "&#x22;": "\"",
        "&#x27;": "'",
        "&#x5C;": "\\",
        "&#x00;": "\0",
        "&#x0C;": "\f",
    };

    for (var controlChar in controlCharacters) {
        var replacement = controlCharacters[controlChar];
        var regex = new RegExp(controlChar, 'g');
        text = text.replace(regex, replacement);
    }

    return text;
}

function prepareToJson(text) {

    text = text.replace(/'/g, '"');
    text = text.replace(/\\\\/g, '\\');
    return text;
}
function generateView(tag, slug, answers, correct) {
    switch (tag) {
        case 'choice':
            generateChoice(slug, answers);
            break;
        case 'parsons':
            generateParson(slug, answers, correct);
            break;
        case 'text':
            generateWordCloud(slug, answers);
            break;
        default:
            break;
    }
}

function generateChoice(slug, answers) {

    var answers_obj = JSON.parse(prepareToJson(answers));

    if (Object.keys(answers_obj).length == 0) {
        return;
    }
    var item_div = document.getElementById(`item-${slug.replace(/\//g, '-')}`);
    item_div.className = "item";


    var canvas = document.createElement("canvas");
    canvas.id = `canvas-${slug}-chart`;

    document.getElementById(slug).appendChild(item_div);
    item_div.appendChild(canvas);

    var barColors = [
        "#b91d47",
        "#00aba9",
        "#2b5797",
        "#e8c3b9",
        "#1e7145"
    ];
    var x = Object.keys(answers_obj)
    var y = [];
    for (var key in answers_obj) {
        y.push(answers_obj[key])
    }
    generateChart(slug, y, x, "pie", barColors);
}


function getWrongLines(answer, correct) {
    var answer_lines = answer.split("\n");
    var correct_lines = correct.split("\n");
    var wrong_lines = [];
    if (correct.length == 0)
        return [];
    for (var i = 0; i < answer_lines.length; i++) {
        if (correct_lines[i] != answer_lines[i])
            wrong_lines.push(i + 1);
    }
    return wrong_lines;
}

function generateParson(slug, answers, correct) {


    var answers_obj = JSON.parse(prepareToJson(answers));

    if (Object.keys(answers_obj).length == 0) {
        return;
    }
    var item_div = document.getElementById(`item-${slug.replace(/\//g, '-')}`);
    item_div.className = "item";

    var canvas = document.createElement("canvas");
    canvas.id = `canvas-${slug}-chart`;

    answer_div = document.createElement("div");
    answer_div.className = "parson-answers";

    document.getElementById(slug).appendChild(item_div);
    item_div.appendChild(canvas);
    item_div.appendChild(answer_div);

    var colors = [];
    var x_values = [];

    for (var answer in answers_obj) {
        var color = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
        colors.push(color);
        x_values.push(answers_obj[answer]);

        var lines = getWrongLines(answer, correct);
        var code_div = document.createElement("div");
        var pre = document.createElement("pre");
        var code = document.createElement("code");

        code.className = "language-python";
        code.innerHTML = answer;
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

    generateChart(slug, x_values, labels, "bar", colors);

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

function generateWordCloud(slug, answers) {

    var answers_obj = JSON.parse(prepareToJson(answers));
    if (Object.keys(answers_obj).length == 0) {
        return;
    }
    var item_div = document.getElementById(`item-${slug.replace(/\//g, '-')}`);
    item_div.className = "item";
    document.getElementById(slug).appendChild(item_div);

    var canvas = document.createElement("canvas");
    canvas.id = `canvas-${slug}`
    item_div.appendChild(canvas);
    WordCloud(document.getElementById(`canvas-${slug}`), { list: answers_obj });



}
