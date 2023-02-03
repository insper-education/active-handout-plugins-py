import Sortable from "sortablejs";

import { removeValue } from "../client-db";
import { markDone, markNotDone } from "../exercise/utils";
import { sendAndCacheData } from "../telemetry";
import {
  queryCorrectAnswer,
  queryDragArea,
  queryDropArea,
  queryParsonsLine,
  queryParsonsLineContainers,
} from "./queries";

export function resetExercise(exercise) {
  removeValue(exercise);
  const slug = exercise.getAttribute("data-slug");
  localStorage.removeItem(`${slug}-drag`);
  localStorage.removeItem(`${slug}-drop`);
  markNotDone(exercise);
  removeResultClasses(exercise);

  const lineContainers = [...queryParsonsLineContainers(exercise)];
  lineContainers.sort((a, b) => a.dataset.linecount - b.dataset.linecount);

  const origArea = queryDragArea(exercise);
  lineContainers.forEach((lineContainer) => {
    origArea.appendChild(lineContainer);
  });
}

export function submitExercise(exercise) {
  removeResultClasses(exercise);

  const origArea = queryDragArea(exercise);
  const answerArea = queryDropArea(exercise);

  const lineContainers = queryParsonsLineContainers(answerArea);
  let correct = false;

  const correctAnswer = queryCorrectAnswer(exercise)?.innerText;
  const hasAnswer = correctAnswer !== undefined;

  let answerText = "";
  lineContainers.forEach((lineContainer) => {
    const line = queryParsonsLine(lineContainer);
    answerText += line.innerText + "\n";
  });
  if (hasAnswer) {
    correct =
      lineContainers.length > 0 &&
      queryParsonsLineContainers(origArea).length === 0;
    correct = correct && answerText === correctAnswer;
  }

  // We need this timeout so the browser has time to reset the
  // exercise before animating again
  setTimeout(() => {
    finishParsonsExercise(exercise, correct, hasAnswer);
  }, 0);
  sendAndCacheData(exercise, { correct, code: answerText }, correct ? 1 : 0);
}

export function finishParsonsExercise(exercise, correct, hasAnswer) {
  markDone(exercise);
  if (correct) {
    exercise.classList.add("correct");
  } else if (hasAnswer) {
    exercise.classList.add("wrong");
  }
}

function removeResultClasses(exercise) {
  exercise.classList.remove("correct");
  exercise.classList.remove("wrong");
}

export function createSortables(slug, dragArea, dropArea) {
  const dropAreaLines = retrieveOrder(`${slug}-drop`);
  dropAreaLines.forEach((lineId) => {
    const lineContainer = document.getElementById(lineId);
    dropArea.appendChild(lineContainer);
  });

  createSortable(dragArea, slug);
  createSortable(dropArea, slug);
}

function createSortable(area, slug) {
  return new Sortable(area, {
    group: slug,
    dataIdAttr: "id",
    store: {
      get: restoreSortable,
      set: saveSortable,
    },
    animation: 150,
  });
}

function retrieveOrder(key) {
  const order = localStorage.getItem(key);
  return order ? order.split("|") : [];
}

function restoreSortable(sortable) {
  const key = getSortableKey(sortable);
  return retrieveOrder(key);
}

function saveSortable(sortable) {
  const key = getSortableKey(sortable);

  const order = sortable.toArray();
  localStorage.setItem(key, order.join("|"));
}

function getSortableKey(sortable) {
  let key = sortable.options.group.name;

  if (sortable.el.classList.contains("parsons-drag-area")) {
    key += "-drag";
  } else {
    key += "-drop";
  }

  return key;
}
