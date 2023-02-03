import {
  queryAddIndentButton,
  queryDragArea,
  queryDropArea,
  queryParsonsExercises,
  queryParsonsLine,
  queryParsonsLineContainers,
  queryRemoveIndentButton,
  queryResetButton,
  querySubmitButton,
} from "./queries";
import {
  addIndent,
  createSortables,
  removeIndent,
  resetExercise,
  saveLineIndentCount,
  submitExercise,
} from "./utils";

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
  const slug = exercise.getAttribute("data-slug");
  const dragArea = queryDragArea(exercise);
  const dropArea = queryDropArea(exercise);
  const lineContainers = queryParsonsLineContainers(exercise);

  createSortables(slug, dragArea, dropArea);

  lineContainers.forEach((lineContainer) => {
    const addIndentBtn = queryAddIndentButton(lineContainer);
    const removeIndentBtn = queryRemoveIndentButton(lineContainer);
    const line = queryParsonsLine(lineContainer);

    addIndentBtn?.addEventListener("click", (event) => {
      event.preventDefault();
      addIndent(line);
      saveLineIndentCount(slug, lineContainer);
      removeIndentBtn.removeAttribute("disabled");
    });

    removeIndentBtn?.addEventListener("click", (event) => {
      event.preventDefault();
      removeIndent(line);
      saveLineIndentCount(slug, lineContainer);
      if (!line.querySelector(".parsons-indent")) {
        removeIndentBtn.setAttribute("disabled", "disabled");
      }
    });
  });

  queryResetButton(exercise)?.addEventListener("click", (event) => {
    event.preventDefault();
    resetExercise(exercise);
  });
  querySubmitButton(exercise).addEventListener("click", (event) => {
    event.preventDefault();
    submitExercise(exercise);
  });
}
