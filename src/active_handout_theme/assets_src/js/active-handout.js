import { initProgressPlugin } from "./progress";
import { initQuestionPlugin } from "./question";

document.addEventListener("DOMContentLoaded", function () {
  let rememberCallbacks = [];
  initProgressPlugin(rememberCallbacks);
  initQuestionPlugin(rememberCallbacks);

  window.addEventListener("remember", function (e) {
    const element = e.detail.element;
    for (let remember of rememberCallbacks) {
      if (remember.match(element)) {
        remember.callback(element);
        break;
      }
    }
  });
});
