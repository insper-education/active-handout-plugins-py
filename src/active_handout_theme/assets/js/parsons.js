function convertRemToPixels(rem) {
    return rem * parseFloat(getComputedStyle(document.documentElement).fontSize);
}

function convertPixelsToRem(px) {
    return px / parseFloat(getComputedStyle(document.documentElement).fontSize);
}

function selectCurrentLine(evt, answerDropArea) {
    const elementsBellowMouse = document.elementsFromPoint(evt.clientX, evt.clientY);
    for (let i = 0; i < elementsBellowMouse.length; i++) {
        if (elementsBellowMouse[i].classList.contains("parsons-line")) {
            return elementsBellowMouse[i];
        }
    }
    return answerDropArea;
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("div.admonition.question.parsons").forEach((exercise) => {
        let dragged = null;

        const answerDropArea = exercise.querySelector(".parsons-drop-area");
        const originalArea = exercise.querySelector(".parsons-drag-area");
        const indentLine = exercise.querySelector(".indent-line");


        const allIndentClasses = Array.from(new Array(10), (x, i) => `indent-level-${i}`);

        answerDropArea.addEventListener("dragover", (e) => {
            e.preventDefault();
            const dropAreaBB = answerDropArea.getBoundingClientRect();
            indentLine.style.display = "block";
            indentLine.style.top = (e.clientY - dropAreaBB.y) + "px";
            const indentLevel = Math.trunc(convertPixelsToRem(e.clientX - dropAreaBB.left) / 2);
            indentLine.classList.remove(...allIndentClasses);
            indentLine.classList.add(`indent-level-${indentLevel}`);

            answerDropArea.querySelectorAll(".parsons-line").forEach((p) => p.classList.remove("line-drop-active"));
            const dropEl = selectCurrentLine(e, answerDropArea);
            if (dropEl === answerDropArea || dropEl.parentElement !== answerDropArea) {
                // answerDropArea.appendChild(dragged);
            } else {
                dropEl.classList.add("line-drop-active");
            }
        });

        answerDropArea.addEventListener("drop", (e) => {
            const draggedParent = dragged.closest(".admonition.parsons");
            if (exercise === draggedParent) {
                dragged.classList.remove(...allIndentClasses);
                answerDropArea.querySelectorAll(".parsons-line").forEach((p) => p.classList.remove("line-drop-active"));
                dragged.remove();

                for (let cls of allIndentClasses) {
                    if (indentLine.className.indexOf(cls) >= 0) {
                        dragged.classList.add(cls);
                        break;
                    }
                }

                const dropEl = selectCurrentLine(e, answerDropArea);
                if (dropEl === answerDropArea || dropEl.parentElement !== answerDropArea) {
                    answerDropArea.appendChild(dragged);
                } else {
                    answerDropArea.insertBefore(dragged, dropEl);
                }

            }
            dragged = null;
            indentLine.style.display = "none";
            e.preventDefault();
        })

        exercise.querySelectorAll(".parsons-line").forEach((line) => {
            line.addEventListener("dragstart", (e) => {
                dragged = e.target;
            });
        });

        exercise.querySelector("input[name=resetButton]").addEventListener("click", () => {
            answerDropArea.querySelectorAll(".parsons-line").forEach((line) => {
                line.remove();
                line.classList.remove(...allIndentClasses);
                originalArea.appendChild(line);
            })
        });

        exercise.querySelector("input[name=sendButton]").addEventListener("click", () => {
            let correct = originalArea.querySelectorAll(".parsons-line").length == 0;
            if (!correct) {
                exercise.classList.remove("wrong");
                void exercise.offsetLeft;
                exercise.classList.add("wrong");
                return;
            }
            answerDropArea.querySelectorAll(".parsons-line").forEach((line, idx) => {
                const correctLineNum = parseInt(line.querySelector("a").id.split("-")[2]);
                const correctIndent = parseInt(line.dataset.indentcount);
                if (correctLineNum !== (idx + 1) ||
                    !line.classList.contains(`indent-level-${correctIndent}`)) {
                    correct = false;
                }
            });
            if (correct) {
                alert("Sua solução está correta!");
            } else {
                exercise.classList.remove("wrong");
                void exercise.offsetLeft;
                exercise.classList.add("wrong");
            }

        });
    });
});

