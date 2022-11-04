export function createElementWithClasses(tagName, classList, parent) {
  const el = document.createElement(tagName);
  for (let className of classList) {
    el.classList.add(className);
  }
  if (parent) {
    parent.appendChild(el);
  }
  return el;
}

export function sendRemember(element, args) {
  const ev = new CustomEvent("remember", { detail: { element, args } });
  window.dispatchEvent(ev);
}

export function deepCopy(dict) {
  return JSON.parse(JSON.stringify(dict));
}

export function listAllElements(parent) {
  let elements = [];
  for (let child of parent.childNodes) {
    elements.push(child);
    elements = elements.concat(listAllElements(child));
  }
  return elements;
}

export function approximatelyEqual(a, b, epsilon) {
  if (!epsilon) epsilon = 0.1;
  return Math.abs(a - b) < epsilon;
}
