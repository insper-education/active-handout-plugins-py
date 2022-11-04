export function queryPlaygrounds() {
  return document.querySelectorAll(".css-playground");
}

export function queryTabs(playground) {
  return playground.querySelectorAll(".file-tab .tab");
}

export function queryEditors(playground) {
  return playground.querySelectorAll(".playground-code-editor");
}

export function queryPreview(playground) {
  return playground.querySelector(".page-preview .preview");
}

export function queryExpectedResult(playground) {
  return playground.querySelector(".page-preview .expected-result");
}

export function queryAnswerFromPlayground(playground) {
  return playground.closest(".css-exercise");
}

export function queryAnswerFiles(answer) {
  return answer.querySelectorAll(".highlight");
}

export function extractFilename(code) {
  let baseName = "index";
  let extension = "css";
  const filenamePattern = "filename-";
  const languagePattern = "language-";
  for (let className of code.classList) {
    if (className.startsWith(filenamePattern))
      baseName = className.substring(filenamePattern.length);
    if (className.startsWith(languagePattern))
      extension = className.substring(languagePattern.length);
  }

  return `${baseName}.${extension}`;
}
