import { getValue, setValue } from "../client-db";

export function initProgressPlugin(rememberCallbacks) {
  rememberCallbacks.push({
    match: (el) => el.classList.contains("progress"),
    callback: (el) => {
      setValue(el, true);
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
