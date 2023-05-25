var last_ex = null;
function generateChart(ex) {
    if (last_ex != null) {
        const element = document.getElementById("canvas-" + last_ex.name);
        element.remove();
    }
    ex = ex.replace(/'/g, '"');
    var exercise = JSON.parse(ex);
    if (exercise.telemetry.x.length == 0){
        last_ex = null;
        return;
    }

    last_ex = exercise;

    var canvas = document.createElement("canvas");
    canvas.id = "canvas-" + exercise.name;

    document.getElementById(exercise.name).appendChild(canvas);  

    var barColors = [
                "#b91d47",
                "#00aba9",
                "#2b5797",
                "#e8c3b9",
                "#1e7145"
                ];
    new Chart("canvas-" + exercise.name, {
    type: "pie",
    data: {
        labels: exercise.telemetry.y,
        datasets: [{
        backgroundColor: barColors,
        data: exercise.telemetry.x
        }]
    },
    options: {
        title: {
            display: true,
            text: exercise.name
        },
        responsive: true,
        maintainAspectRatio: false,
    }
    });
}

function generateParson(ex){
    if (last_ex != null) {
        const element = document.getElementById("canvas-" + last_ex.name);
        element.remove();
    }   
    console.log("here here");
    ex = ex.replace(/'/g, '"');
    var exercise = JSON.parse(ex);
    if (exercise.telemetry.x.length == 0){
        last_ex = null;
        return;
    }

    last_ex = exercise;

    var pre = document.createElement("pre");
    var code = document.createElement("code");
    pre.id = "canvas-" + exercise.name;
    code.className = "language-python";
    pre.className = "language-python";
    code.innerHTML = Prism.highlight(exercise.telemetry.y[0], Prism.languages.python, 'python');

    document.getElementById(exercise.name).appendChild(pre);
    pre.appendChild(code);  

}