import {
  queryDragArea,
  queryDropArea,
  queryParsonsExercises,
  queryParsonsLines,
} from "./queries";

export function initParsonsPlugin(rememberCallbacks) {
  queryParsonsExercises().forEach((exercise) => {
    const destArea = queryDropArea(exercise);
    const origArea = queryDragArea(exercise);
    const areas = [origArea, destArea];
    const destContainer = destArea.closest(".parsons-container");
    const origContainer = origArea.closest(".parsons-container");
    const containers = [origContainer, destContainer];
    const ctx = {
      dragged: null,
      exercise,
      areas,
      destArea,
      origArea,
      containers,
      destContainer,
      origContainer,
    };
    ctx.onDrag = makeDragEnterContainer(ctx);
    ctx.onDrop = makeDropListener(ctx);

    queryParsonsLines(exercise).forEach((line) => {
      line.addEventListener("dragstart", makeDragStart(ctx));
    });
  });
}

function makeDragEnterContainer({ containers, exercise }) {
  return (ev) => {
    ev.preventDefault();

    const slot = selectCurrentSlot(ev, exercise);

    if (slot) {
      setDragOver(slot, exercise);
      shiftLines(slot);

      containers.forEach((otherContainer) => {
        otherContainer.classList.remove("drag-over");
      });
      slot.closest(".parsons-container").classList.add("drag-over");
    }
  };
}

function makeDragStart(ctx) {
  return (ev) => {
    window.addEventListener("dragenter", ctx.onDrag);
    window.addEventListener("dragover", ctx.onDrag);
    window.addEventListener("drop", ctx.onDrop);

    const line = ev.target;
    for (let area of ctx.areas) {
      area.appendChild(createLineSlot(ctx));
    }

    setDragging(line);
    ctx.dragged = line;
  };
}

function createLineSlot(ctx) {
  const lineSlot = document.createElement("div");
  lineSlot.classList.add("line-slot");

  return lineSlot;
}

function setDragging(target) {
  setTimeout(() => {
    // We need this timeout because the element is copied to
    // be displayed as an image while dragging
    target.closest(".line-slot").classList.add("dragging");
  }, 0);
}

function cleanUpSlots(exercise) {
  const slots = exercise.querySelectorAll(".line-slot");
  for (let slot of slots) {
    slot.classList.remove("dragging");
    if (slot.querySelectorAll(".parsons-line").length === 0) {
      slot.remove();
    }
  }
}

function selectElementWithClass(ev, className) {
  const elementsBellowMouse = document.elementsFromPoint(
    ev.clientX,
    ev.clientY
  );
  for (let i = 0; i < elementsBellowMouse.length; i++) {
    if (elementsBellowMouse[i].classList.contains(className)) {
      return elementsBellowMouse[i];
    }
  }
}

function selectCurrentSlot(ev, exercise) {
  let slot = selectElementWithClass(ev, "line-slot");
  if (slot) return slot;
  const container = selectElementWithClass(ev, "parsons-container");
  if (container) return container.querySelector(".line-slot:not(.with-line)");
  return exercise.querySelector(".line-slot.drag-over");
}

function shiftLines(slot) {
  if (!slot.classList.contains("with-line")) return;

  const area = slot.closest(".parsons-area");
  const emptySlot = selectEmptySlot(area);

  if (emptyIsBefore(area, emptySlot, slot)) {
    area.insertBefore(emptySlot, slot.nextSibling);
  } else {
    area.insertBefore(emptySlot, slot);
  }
}

function selectEmptySlot(area) {
  return area.querySelector(".line-slot:not(.with-line)");
}

function emptyIsBefore(area, emptySlot, refSlot) {
  for (let slot of area.querySelectorAll(".line-slot")) {
    if (slot === emptySlot) return true;
    if (slot === refSlot) return false;
  }
  return false;
}

function insertLineInSlot(slot, ctx) {
  const prevSlot = ctx.dragged.closest(".line-slot");
  slot.appendChild(ctx.dragged);
  slot.classList.remove("drag-over");
  slot.classList.add("with-line");
  ctx.dragged = null;
  prevSlot.remove();
}

function setDragOver(slot, exercise) {
  slot.classList.add("drag-over");
  exercise.querySelectorAll(".line-slot").forEach((other) => {
    if (other !== slot) other.classList.remove("drag-over");
  });
}

function makeDropListener(ctx) {
  return (ev) => {
    ev.preventDefault();

    window.removeEventListener("dragenter", ctx.onDrag);
    window.removeEventListener("dragover", ctx.onDrag);
    window.removeEventListener("drop", ctx.onDrop);

    const slot = selectCurrentSlot(ev, ctx.exercise);

    if (slot) {
      insertLineInSlot(slot, ctx);
    }

    ctx.containers.forEach((container) =>
      container.classList.remove("drag-over")
    );

    cleanUpSlots(ctx.exercise);
  };
}
