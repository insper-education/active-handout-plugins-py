import { initTabbedPlugin } from "./tabbed-content";
import { initProgressPlugin } from "./progress";
import { initExercisePlugin } from "./exercise";

function onLoad() {
  initTabbedPlugin();

  let rememberCallbacks = [];

  window.addEventListener("remember", function (e) {
    const element = e.detail.element;
    for (let remember of rememberCallbacks) {
      if (remember.match(element)) {
        remember.callback(element);
        break;
      }
    }
  });

  initProgressPlugin(rememberCallbacks);
  initExercisePlugin(rememberCallbacks);
}

if (document.readyState !== "loading") {
  onLoad();
} else {
  document.addEventListener("DOMContentLoaded", onLoad);
}
