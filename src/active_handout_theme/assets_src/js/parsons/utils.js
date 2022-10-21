import { createElementWithClasses } from "../dom-utils";
import {
  queryAreaFromInside,
  queryContainerFromInside,
  queryEmptySlot,
  queryLastSlot,
  queryParsonsContainers,
  queryParsonsLines,
  querySlotFromInside,
  querySlots,
  querySubslots,
} from "./queries";

export function addDragListeners(onDrag, onDrop) {
  window.removeEventListener("dragenter", onDrag);
  window.removeEventListener("dragover", onDrag);
  window.removeEventListener("drop", onDrop);
}

export function removeDragListeners(onDrag, onDrop) {
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

function getIndentCount(subslot) {
  const prefix = "subslot-";

  for (let className of subslot.classList) {
    if (className.startsWith(prefix)) {
      const count = parseInt(className.substr(prefix.length));
      if (count) return count - 1;
    }
  }
  return 0;
}
