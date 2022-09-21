function keyFromElement(el) {
  const docAddr = document.location.pathname;
  return `${docAddr}/${el.id}`;
}

function saveAndSendData(key, value) {
  localStorage[key] = value;
  let dataCollectionURL = "{{ config.extra.telemetry_url }}";
  // TODO: fetch POST with token
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("a.progress").forEach((e) => {
    const k = keyFromElement(e);
    if (localStorage.getItem(k) !== null) {
      e.click();
    }
  });

  document
    .querySelectorAll(
      "div.admonition.question.short, " +
        "div.admonition.question.medium, " +
        "div.admonition.question.long"
    )
    .forEach((e) => {
      const k = keyFromElement(e);
      const itemValue = localStorage.getItem(k);
      if (itemValue !== null) {
        e.querySelector("input[name='data'], textarea[name='data']").value =
          itemValue;
        e.querySelector("input[type='submit']").click();
      }
    });

  document.querySelectorAll("div.admonition.question.choice").forEach((e) => {
    const k = keyFromElement(e);
    const itemValue = localStorage.getItem(k);
    if (itemValue !== null) {
      e.querySelector(`input[name='data'][value='${itemValue}'`).checked = true;
      e.querySelector("input[type='submit']").click();
    }
  });

  document.querySelectorAll("div.admonition.exercise").forEach((e) => {
    const k = keyFromElement(e);
    const itemValue = localStorage.getItem(k);
    if (itemValue !== null) {
      e.querySelector("input[type='submit']").click();
    }
  });

  window.addEventListener("remember", function (e) {
    const element = e.detail.element;
    if (element.classList.contains("progress")) {
      saveAndSendData(keyFromElement(element), true);
    } else if (element.classList.contains("choice")) {
      const choices = element.querySelectorAll(
        "input[name='data'][type='radio']"
      );
      for (let choice of choices) {
        if (choice.checked) {
          saveAndSendData(keyFromElement(element), choice.value);
        }
      }
    } else if (
      element.classList.contains("short") ||
      element.classList.contains("medium") ||
      element.classList.contains("long")
    ) {
      const textElement = element.querySelector(
        "input[name='data'], textarea[name='data']"
      );
      saveAndSendData(keyFromElement(element), textElement.value);
    } else if (element.classList.contains("exercise")) {
      saveAndSendData(keyFromElement(element), true);
    }
  });
});
