import Sortable from "sortablejs";

import {
  queryAddIndentButton,
  queryDragArea,
  queryDropArea,
  queryParsonsExercises,
  queryParsonsLine,
  queryParsonsLineContainers,
  queryRemoveIndentButton,
} from "./queries";

const DROP_AREA_SLOTS = 6;

export function initParsonsPlugin() {
  queryParsonsExercises().forEach((exercise) => {
    registerListeners(exercise);
    // recoverPreviousState(exercise, DROP_AREA_SLOTS);
    // const { value: prevAnswer, submitted } = getSubmissionCache(exercise);
    // if (prevAnswer !== null) {
    //   finishParsonsExercise(exercise, prevAnswer.correct);
    //   if (!submitted) {
    //     sendAndCacheData(exercise, prevAnswer, prevAnswer.correct ? 1 : 0);
    //   }
    // }
  });
}

function registerListeners(exercise) {
  const dragArea = queryDragArea(exercise);
  const dropArea = queryDropArea(exercise);
  const lineContainers = queryParsonsLineContainers(exercise);

  new Sortable(dragArea, {
    group: exercise.id,
    animation: 150,
  });

  new Sortable(dropArea, {
    group: exercise.id,
    animation: 150,
  });

  lineContainers.forEach((lineContainer) => {
    const addIndentBtn = queryAddIndentButton(lineContainer);
    const removeIndentBtn = queryRemoveIndentButton(lineContainer);
    const line = queryParsonsLine(lineContainer);
    const lineAnchor = line.querySelector("a");

    addIndentBtn.addEventListener("click", (event) => {
      event.preventDefault();
      const indent = document.createElement("span");
      indent.classList.add("parsons-indent");
      indent.innerText = "    ";

      line.insertBefore(indent, lineAnchor.nextSibling);

      removeIndentBtn.removeAttribute("disabled");
    });

    removeIndentBtn.addEventListener("click", (event) => {
      event.preventDefault();
      line.querySelector(".parsons-indent")?.remove();

      if (!line.querySelector(".parsons-indent")) {
        removeIndentBtn.setAttribute("disabled", "disabled");
      }
    });
  });
}
