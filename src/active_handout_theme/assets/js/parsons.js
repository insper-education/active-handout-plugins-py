function createElementWithAttributes(tag, attributes) {
    const e = document.createElement(tag);
    for (const [attr, val] of Object.entries(attributes)) {
        e.setAttribute(attr, val);
    }
    return e;
}

function findIndentLevel(line, tabSize) {
    let spaces = 0;
    for (const c of line) {
        if (c != ' ') break;
        spaces++;
    }
    return Math.floor(spaces / tabSize);
}

function splitCodeIntoLI(codeString) {
    const items = [];
    let count = 0;

    for (const line of codeString.split("\n")) {
        const noSpaces = line.trim();
        if (noSpaces === "") continue;

        const indentLevel = findIndentLevel(line, 4);
        const newLI = createElementWithAttributes('li', {'draggable': true, "data-indent": indentLevel, "data-order": count});
        newLI.innerText = line.substring(indentLevel * 4);
        items.push(newLI);

        count++;
     }

    return items;
}

let i = splitCodeIntoLI(`
def py(as):
    print(as)
    return as + 3;
`);



const l = document.getElementById("p");
for (const ll of i) {
    l.appendChild(ll);
}
const answerBox = document.getElementById("answerBox");

let dragged = null;

for (const c of l.children) {
    c.draggable = true;
    c.addEventListener("dragstart", (e) => {
        dragged = e.target;
    });
}



answerBox.addEventListener("dragover", (event) => {
  // prevent default to allow drop
  event.preventDefault();
});

answerBox.addEventListener("drop", (e) => {
    const dropEl = document.elementFromPoint(e.clientX, e.clientY);
    
    const answerBoxBound = answerBox.getBoundingRect();
    
    // TODO: indentLevel relativo ao answerBox!!
    const elementX = e.pageX - answerBox.left;
    const indentLevel = Math.round(e.clientX / 70);
    console.log(elementX);
    dragged.className = `indent${indentLevel}`;

    if (dropEl === dragged) return true;

    dragged.remove();
    if (dropEl !== answerBox) {
        answerBox.insertBefore(dragged, dropEl);
    } else {
        answerBox.append(dragged);
    }

    dragged = null;
    return true;
});


document.getElementById("check").addEventListener("click", (e) => {
    let counter = 0;
    for (const c of answerBox.children) {
        if (c.dataset["order"] == counter) console.log(`linha ${counter} no lugar certo!`);
        else console.log("linha no lugar errado!");
        
        const expectedIndent = c.dataset["indent"];
        if (c.classList.contains(`indent${expectedIndent}`)) console.log(`linha ${counter} indentação correta!`);
        else console.log("indentação incorreta");
             
        counter++;
    }
});
