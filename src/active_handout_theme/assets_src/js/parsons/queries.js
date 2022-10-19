export function queryParsonsExercises() {
  return document.querySelectorAll("div.admonition.exercise.parsons");
}

export function queryDropArea(exercise) {
  return exercise.querySelector(".parsons-drop-area");
}

export function queryDragArea(exercise) {
  return exercise.querySelector(".parsons-drag-area");
}

export function queryParsonsLines(exercise) {
  return exercise.querySelectorAll(".parsons-line");
}
