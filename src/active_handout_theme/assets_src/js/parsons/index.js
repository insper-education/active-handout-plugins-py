import {
  queryDragArea,
  queryDropArea,
  queryParsonsExercises,
  queryParsonsLines,
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
} from "./utils";

export function initParsonsPlugin(rememberCallbacks) {
  queryParsonsExercises().forEach(registerListeners);
}

function registerListeners(exercise) {
  const destArea = queryDropArea(exercise);
  const origArea = queryDragArea(exercise);
  let draggedLine = null;

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
