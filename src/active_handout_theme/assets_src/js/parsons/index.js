import {
  queryDragArea,
  queryDropArea,
  queryParsonsExercises,
  queryParsonsLines,
  selectSlotUnderCursor,
} from "./queries";
import {
  addDragListeners,
  cleanUpSlots,
  createSlots,
  hide,
  insertLineInSlot,
  removeDragListeners,
  setCurrentSlot,
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
    setCurrentSlot(selectSlotUnderCursor(ev, exercise), exercise);
  }

  function onDrop(ev) {
    ev.preventDefault();
    addDragListeners(onDrag, onDrop);

    insertLineInSlot(draggedLine, selectSlotUnderCursor(ev, exercise));
    cleanUpSlots(exercise);
    draggedLine = null;
  }

  function onDragStart(ev) {
    removeDragListeners(onDrag, onDrop);

    createSlots([origArea, destArea]);

    draggedLine = ev.target;
    hide(draggedLine);
  }

  queryParsonsLines(exercise).forEach((line) => {
    line.addEventListener("dragstart", onDragStart);
  });
}
