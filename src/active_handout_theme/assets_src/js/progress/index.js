import { getValue } from "../client-db";
import { saveAndSendData } from "../telemetry";

export function initProgressPlugin(rememberCallbacks) {
  queryProgressBtns().forEach((e) => {
    if (getValue(e)) {
      e.click();
    }
  });

  rememberCallbacks.push({
    match: (el) => el.classList.contains("progress"),
    callback: (el) => {
      saveAndSendData(el, true);
    },
  });
}

function queryProgressBtns() {
  return document.querySelectorAll("button.progress");
}
