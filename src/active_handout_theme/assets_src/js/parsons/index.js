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
import { sendData } from "../telemetry";
import { setValue } from "../client-db";

export function initParsonsPlugin(rememberCallbacks) {
  queryParsonsExercises().forEach(registerListeners);

  rememberCallbacks.push({
    match: (el) => el.classList.contains("parsons"),
    callback: (el, user, { correct, code }) => {
      const value = JSON.stringify({ correct, code });
      setValue(el, value);
      sendData(el, value, correct ? 1 : 0, user);
      return true;
    },
  });
}

function registerListeners(exercise) {
  const destArea = queryDropArea(exercise);
  const origArea = queryDragArea(exercise);
  let draggedLine = null;

  queryResetButton(exercise).addEventListener("click", () =>
    resetExercise(exercise)
  );

  querySubmitButton(exercise).addEventListener("click", () =>
    submitExercise(exercise)
  );

  function onDrag(ev) {
    ev.preventDefault();
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
