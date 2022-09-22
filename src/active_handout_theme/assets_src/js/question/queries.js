export function queryTextQuestions() {
  return document.querySelectorAll(
    "div.admonition.question.short, " +
      "div.admonition.question.medium, " +
      "div.admonition.question.long"
  );
}

export function queryChoiceQuestions() {
  return document.querySelectorAll("div.admonition.question.choice");
}

export function queryExercises() {
  return document.querySelectorAll("div.admonition.exercise");
}

export function queryTextInputs(el) {
  return el.querySelector("input[name='data'], textarea[name='data']");
}

export function queryOptions(el) {
  return el.querySelectorAll("input[name='data'][type='radio']");
}

export function queryOption(el, value) {
  return el.querySelector(`input[name='data'][value='${value}'`);
}

export function querySubmitBtn(el) {
  return el.querySelector("input[type='submit']");
}
