import { initTabbedPlugin } from "./tabbed-content";
import { initProgressPlugin } from "./progress";
import { initMenuPlugin } from "./menu";
import { initExercisePlugin } from "./exercise";
import { initFooterPlugin } from "./footnote";
import { initParsonsPlugin } from "./parsons";
import { initStyle } from "./style";
import { initAuth } from "./auth";
import { initCodeEditorPlugin } from "./code-editor";

function onLoad() {
  let rememberCallbacks = [];

  const user = initAuth();
  window.addEventListener("remember", function (e) {
    const element = e.detail.element;
    for (let remember of rememberCallbacks) {
      if (remember.match(element)) {
        const stop = remember.callback(element, user, e.detail.args);
        if (stop) break;
      }
    }
  });

  initTabbedPlugin();

  initStyle();
  initProgressPlugin(rememberCallbacks);
  initParsonsPlugin(rememberCallbacks);
  initExercisePlugin(rememberCallbacks);
  initFooterPlugin(rememberCallbacks);
  initMenuPlugin();
  initCodeEditorPlugin();
}

if (document.readyState !== "loading") {
  onLoad();
} else {
  document.addEventListener("DOMContentLoaded", onLoad);
}
