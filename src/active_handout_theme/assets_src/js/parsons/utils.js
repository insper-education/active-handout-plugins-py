import { createElementWithClasses, sendRemember } from "../dom-utils";
import {
  queryAnswer,
  queryAreaFromInside,
  queryContainerFromInside,
  queryDragArea,
  queryDropArea,
  queryEmptySlot,
  queryLastSlot,
  queryParsonsContainers,
  queryParsonsLines,
  querySlotFromInside,
  querySlots,
  querySubslots,
  selectExerciseUnderCursor,
} from "./queries";

export function removeDragListeners(onDrag, onDrop) {
  window.removeEventListener("dragenter", onDrag);
  window.removeEventListener("dragover", onDrag);
  window.removeEventListener("drop", onDrop);
}

export function addDragListeners(onDrag, onDrop) {
  window.addEventListener("dragenter", onDrag);
  window.addEventListener("dragover", onDrag);
  window.addEventListener("drop", onDrop);
}

export function insertLineInSubslot(line, subslot) {
  if (!subslot) return;

  const slot = querySlotFromInside(subslot);
  slot.classList.remove("drag-over");
  slot.classList.add("with-line");
  subslot.classList.remove("drag-over");
  subslot.classList.add("cur-indent");

  slot.appendChild(line);
}

export function eventIsInsideExercise(ev, exercise) {
  return selectExerciseUnderCursor(ev) === exercise;
}

export function setCurrentSubslot(subslot, exercise) {
  if (!subslot) return;

  const slot = querySlotFromInside(subslot);
  slot.classList.add("drag-over");
  subslot.classList.add("drag-over");

  querySlots(exercise).forEach((other) => {
    if (other !== slot) other.classList.remove("drag-over");
  });
  querySubslots(exercise).forEach((other) => {
    if (other !== subslot) other.classList.remove("drag-over");
  });

  shiftLines(slot);

  const container = queryContainerFromInside(slot);
  const containers = queryParsonsContainers(exercise);
  resetContainers(containers, container);
  container.classList.add("drag-over");
}

export function createSlot(area, subslotCount, additionalClass) {
  const slot = createElementWithClasses("div", ["line-slot"], area);
  const classList = ["subslot"];
  if (additionalClass) classList.push(additionalClass);
  for (let i = 0; i < subslotCount; i++) {
    createElementWithClasses("div", [...classList, `subslot-${i + 1}`], slot);
  }
  createElementWithClasses("div", ["line-placeholder"], slot);
}

export function hide(line) {
  setTimeout(() => {
    // We need this timeout because the element is copied to
    // be displayed as an image while dragging.
    // The timeout postpones hiding the slot (add .dragging).
    querySlotFromInside(line).classList.add("dragging");
  }, 0);
}

export function cleanUpSlots(exercise) {
  const slots = querySlots(exercise);
  for (let slot of slots) {
    slot.classList.remove("dragging");
    if (queryParsonsLines(slot).length === 0) {
      slot.remove();
    }
  }
}

export function resetExercise(exercise) {
  hideAnswer(queryAnswer(exercise));

  const origArea = queryDragArea(exercise);
  const destArea = queryDropArea(exercise);
  queryParsonsLines(destArea).forEach((line) => {
    const slot = querySlotFromInside(line);
    const newSlot = createElementWithClasses(
      "div",
      ["line-slot", "with-line"],
      origArea
    );
    createElementWithClasses(
      "div",
      ["subslot", "cur-indent", "single-subslot"],
      newSlot
    );
    createElementWithClasses("div", ["line-placeholder"], newSlot);
    newSlot.appendChild(line);
    slot.remove();
  });
}

export function submitExercise(exercise) {
  exercise.classList.remove("correct");
  exercise.classList.remove("wrong");

  const origArea = queryDragArea(exercise);
  const answerArea = queryDropArea(exercise);

  const lines = queryParsonsLines(answerArea);
  let correct = lines.length > 0 && queryParsonsLines(origArea).length === 0;
  lines.forEach((line, idx) => {
    const slot = querySlotFromInside(line);

    const correctLineNum = getLineNumber(line);
    const isCorrectLine = correctLineNum === idx + 1;

    const correctIndent = parseInt(line.dataset.indentcount);
    const isCorrectIndent = correctIndent === getIndentCount(slot);

    correct &&= isCorrectLine && isCorrectIndent;
  });

  // We need this timeout so the browser has time to reset the
  // exercise before animating again
  setTimeout(() => {
    if (correct) {
      exercise.classList.add("correct");
    } else {
      exercise.classList.add("wrong");
    }
  }, 0);
  showAnswer(queryAnswer(exercise));

  sendRemember(exercise, { correct });
}

function getLineNumber(line) {
  return parseInt(line.querySelector("a").id.split("-")[2]);
}

function resetContainers(containers, exceptThis) {
  containers.forEach((otherContainer) => {
    if (otherContainer !== exceptThis) {
      shiftLines(queryLastSlot(otherContainer));
    }
  });
}

function shiftLines(slot) {
  if (!slot.classList.contains("with-line")) return;

  const area = queryAreaFromInside(slot);
  const emptySlot = queryEmptySlot(area);

  if (emptyIsBeforeRef(area, emptySlot, slot)) {
    area.insertBefore(emptySlot, slot.nextSibling);
  } else {
    area.insertBefore(emptySlot, slot);
  }
}

function emptyIsBeforeRef(area, emptySlot, refSlot) {
  for (let slot of querySlots(area)) {
    if (slot === emptySlot) return true;
    if (slot === refSlot) return false;
  }
  return false;
}

function getIndentCount(slot) {
  const subslot = slot.querySelector(".subslot.cur-indent");
  const prefix = "subslot-";
  for (let className of subslot.classList) {
    if (className.startsWith(prefix)) {
      const count = parseInt(className.substr(prefix.length));
      if (count) return count - 1;
    }
  }
  return 0;
}

function showAnswer(answer) {
  answer.style.display = "inherit";
}

function hideAnswer(answer) {
  answer.style.display = "none";
}
