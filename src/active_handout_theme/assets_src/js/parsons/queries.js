export function queryParsonsExercises() {
  return document.querySelectorAll("div.admonition.exercise.parsons");
}

export function queryDragArea(exercise) {
  return exercise.querySelector(".parsons-drag-area");
}

export function queryDropArea(exercise) {
  return exercise.querySelector(".parsons-drop-area");
}

export function queryParsonsLineContainers(container) {
  return container.querySelectorAll(".parsons-line-container");
}

export function queryParsonsLine(container) {
  return container.querySelector(".parsons-line");
}

export function queryAddIndentButton(container) {
  return container.querySelector(".indent-btn--add");
}

export function queryRemoveIndentButton(container) {
  return container.querySelector(".indent-btn--remove");
}
