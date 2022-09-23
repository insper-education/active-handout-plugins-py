import { initTabbedPlugin } from "./tabbed-content";
import { initProgressPlugin } from "./progress";
import { initQuestionPlugin } from "./question";

function onLoad() {
  initTabbedPlugin();

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
}

if (document.readyState !== "loading") {
  onLoad();
} else {
  document.addEventListener("DOMContentLoaded", onLoad);
}
