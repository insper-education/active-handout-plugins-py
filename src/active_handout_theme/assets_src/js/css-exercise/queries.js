export function queryPlaygrounds() {
  return document.querySelectorAll(".css-playground");
}

export function queryEditors(playground) {
  return playground.querySelectorAll(".playground-code-editor");
}
