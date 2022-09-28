import { getValue } from "../client-db";
import { saveAndSendData } from "../telemetry";

export function initProgressPlugin(rememberCallbacks) {
  rememberCallbacks.push({
    match: (el) => el.classList.contains("progress"),
    callback: (el) => {
      saveAndSendData(el, true);
    },
  });

  queryProgressBtns().forEach((e) => {
    if (getValue(e)) {
      e.click();
    }
  });
}

function queryProgressBtns() {
  return document.querySelectorAll("button.progress");
}
