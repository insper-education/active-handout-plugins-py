import { initTabbedPlugin } from "./tabbed-content";
import { initProgressPlugin } from "./progress";
import { initMenuPlugin } from "./menu";
import { initExercisePlugin } from "./exercise";
import { initFooterPlugin } from "./footnote";
import { initStyle } from "./style";

function onLoad() {
  initTabbedPlugin();

  let rememberCallbacks = [];

  window.addEventListener("remember", function (e) {
    const element = e.detail.element;
    for (let remember of rememberCallbacks) {
      if (remember.match(element)) {
        remember.callback(element);
      }
    }
  });

  initStyle();
  initMenuPlugin(rememberCallbacks);
  initProgressPlugin(rememberCallbacks);
  initExercisePlugin(rememberCallbacks);
  initFooterPlugin(rememberCallbacks);
}

if (document.readyState !== "loading") {
  onLoad();
} else {
  document.addEventListener("DOMContentLoaded", onLoad);
}
