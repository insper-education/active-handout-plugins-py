import { markNotDone } from "../exercise/utils";
import { getSubmissionCache, sendAndCacheData } from "../telemetry";
import {
  queryDragArea,
  queryDropArea,
  queryParsonsExercises,
  queryParsonsLines,
  queryResetButton,
  querySubmitButton,
  selectSubslotUnderCursor,
} from "./queries";
import {
  removeDragListeners,
  cleanUpSlots,
  createSlot,
  eventIsInsideExercise,
  hide,
  insertLineInSubslot,
  addDragListeners,
  setCurrentSubslot,
  resetExercise,
  submitExercise,
} from "./utils";

export function initParsonsPlugin() {
  queryParsonsExercises().forEach((exercise) => {
    registerListeners(exercise);

    const { value: prevAnswer, submitted } = getSubmissionCache(exercise);
    if (prevAnswer !== null && !submitted) {
      sendAndCacheData(exercise, prevAnswer, prevAnswer.correct ? 1 : 0);
    }
  });
}

function registerListeners(exercise) {
  const destArea = queryDropArea(exercise);
  const origArea = queryDragArea(exercise);
  let draggedLine = null;

  queryResetButton(exercise).addEventListener("click", (event) => {
    event.preventDefault();
    resetExercise(exercise);
  });
  querySubmitButton(exercise).addEventListener("click", (event) => {
    event.preventDefault();
    submitExercise(exercise);
  });

  function onDrag(ev) {
    ev.preventDefault();
    markNotDone(exercise);

    if (!eventIsInsideExercise(ev, exercise)) return;
    setCurrentSubslot(selectSubslotUnderCursor(ev, exercise), exercise);
  }

  function onDrop(ev) {
    ev.preventDefault();
    removeDragListeners(onDrag, onDrop);

    if (eventIsInsideExercise(ev, exercise)) {
      insertLineInSubslot(draggedLine, selectSubslotUnderCursor(ev, exercise));
    }
    cleanUpSlots(exercise);
    draggedLine = null;
  }

  function onDragStart(ev) {
    addDragListeners(onDrag, onDrop);

    createSlot(origArea, 1, "single-subslot");
    createSlot(destArea, 6);

    draggedLine = ev.target;
    hide(draggedLine);
  }

  queryParsonsLines(exercise).forEach((line) => {
    line.addEventListener("dragstart", onDragStart);
  });
}
