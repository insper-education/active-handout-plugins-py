import { initTabbedPlugin } from "./tabbed-content";
import { initProgressPlugin } from "./progress";
import { initMenuPlugin } from "./menu";
import { initExercisePlugin } from "./exercise";
import { initFooterPlugin } from "./footnote";
import { initParsonsPlugin } from "./parsons";
import { initStyle } from "./style";
import { initAuth } from "./auth";
import { initCodeEditorPlugin } from "./code-editor";
import * as clientDB from "./client-db";
import { sendData } from "./telemetry";

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

  applyRegisteredInitializers();
}

function applyRegisteredInitializers() {
  window.initializers.forEach((initialize) => initialize());
  window.initialized = true;
}

window.clientDB = clientDB;
window.sendData = sendData;

if (document.readyState !== "loading") {
  onLoad();
} else {
  document.addEventListener("DOMContentLoaded", onLoad);
}
