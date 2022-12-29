import { getValue, removeValue, setValue } from "../client-db";
import { sendData } from "../telemetry";
import {
  queryChoiceExercises,
  querySelfProgressExercises,
  queryOption,
  queryOptions,
  querySubmitBtn,
  queryTextInputs,
  queryTextExercises,
  queryCorrectOptionIdx,
  queryParentAlternative,
} from "./queries";

export function initExercisePlugin(rememberCallbacks) {
  rememberCallbacks.push(
    {
      match: matchTextExercises,
      callback: rememberTextExercise,
    },
    {
      match: matchChoiceExercises,
      callback: rememberChoiceExercise,
    },
    {
      match: matchSelfProgressExercises,
      callback: rememberSelfProgressExercise,
    }
  );

  initTextExercises();
  initChoiceExercises();
  initSelfProgressExercises();

  const resetHandoutButton = document.getElementById("resetHandoutButton");

  if (resetHandoutButton) {
    resetHandoutButton.addEventListener("click", function () {
      const exercises = document.querySelectorAll(".admonition.exercise");
      for (const ex of exercises) {
        removeValue(ex);
      }
      location.reload();
    });
  }
}

function initTextExercises() {
  queryTextExercises().forEach((el) => {
    const prevAnswer = getValue(el);
    if (prevAnswer !== null) {
      const input = queryTextInputs(el);
      input.value = prevAnswer;
      const growWrap = input.closest(".grow-wrap");
      if (growWrap) {
        growWrap.dataset.replicatedValue = prevAnswer;
      }

      querySubmitBtn(el).click();
    }
  });
}

function matchTextExercises(el) {
  return (
    el.classList.contains("short") ||
    el.classList.contains("medium") ||
    el.classList.contains("long")
  );
}

function rememberTextExercise(el, user) {
  const textElement = queryTextInputs(el);
  setValue(element, textElement.value);
  sendData(element, textElement.value, 0, user);
  return true;
}

function initChoiceExercises() {
  queryChoiceExercises().forEach((el) => {
    const prevAnswer = getValue(el);
    if (prevAnswer !== null) {
      const option = queryOption(el, prevAnswer);
      const alternative = queryParentAlternative(option);
      option.setAttribute("checked", true);
      alternative.classList.add("selected");
      const submitBtn = querySubmitBtn(el);
      submitBtn.disabled = false;
      submitBtn.click();
    }
  });
}

function matchChoiceExercises(el) {
  return el.classList.contains("choice");
}

function rememberChoiceExercise(el, user) {
  const choices = queryOptions(el);
  const correctIdx = queryCorrectOptionIdx(el);
  for (let choice of choices) {
    const alternative = queryParentAlternative(choice);
    if (correctIdx === choice.value) {
      alternative.classList.add("correct");
    } else {
      alternative.classList.add("wrong");
    }

    if (choice.checked) {
      const points = correctIdx === choice.value ? 1 : 0;
      setValue(el, choice.value);
      sendData(el, choice.value, points, user);
    }
  }

  return true;
}

function initSelfProgressExercises() {
  querySelfProgressExercises().forEach((el) => {
    const prevAnswer = getValue(el);
    if (prevAnswer !== null) {
      querySubmitBtn(el).click();
    }
  });
}

function matchSelfProgressExercises(el) {
  return el.classList.contains("self-progress");
}

function rememberSelfProgressExercise(el, user) {
  setValue(el, true);
  sendData(el, true, 0, user);
  return true;
}
