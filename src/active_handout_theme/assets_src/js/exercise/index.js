import { getValue } from "../client-db";
import { saveAndSendData } from "../telemetry";
import {
  queryChoiceExercises,
  querySelfProgressExercises,
  queryOption,
  queryOptions,
  querySubmitBtn,
  queryTextInputs,
  queryTextExercises,
} from "./queries";

export function initExercisePlugin(rememberCallbacks) {
  initTextExercises(rememberCallbacks);
  initChoiceExercises(rememberCallbacks);
  initSelfProgressExercises(rememberCallbacks);
}

function initTextExercises(rememberCallbacks) {
  queryTextExercises().forEach((el) => {
    const prevAnswer = getValue(el);
    if (prevAnswer !== null) {
      queryTextInputs(el).value = prevAnswer;
      querySubmitBtn(el).click();
    }
  });

  rememberCallbacks.push({
    match: (el) =>
      el.classList.contains("short") ||
      el.classList.contains("medium") ||
      el.classList.contains("long"),
    callback: (el) => {
      const textElement = queryTextInputs(el);
      saveAndSendData(element, textElement.value);
    },
  });
}

function initChoiceExercises(rememberCallbacks) {
  queryChoiceExercises().forEach((el) => {
    const prevAnswer = getValue(el);
    if (prevAnswer !== null) {
      queryOption(el, prevAnswer).checked = true;
      querySubmitBtn(el).click();
    }
  });

  rememberCallbacks.push({
    match: (el) => el.classList.contains("choice"),
    callback: (el) => {
      const choices = queryOptions(el);
      for (let choice of choices) {
        if (choice.checked) {
          saveAndSendData(el, choice.value);
        }
      }
    },
  });
}

function initSelfProgressExercises(rememberCallbacks) {
  querySelfProgressExercises().forEach((el) => {
    const prevAnswer = getValue(el);
    if (prevAnswer !== null) {
      querySubmitBtn(el).click();
    }
  });

  rememberCallbacks.push({
    match: (el) => el.classList.contains("exercise"),
    callback: (el) => {
      saveAndSendData(el, true);
    },
  });
}
