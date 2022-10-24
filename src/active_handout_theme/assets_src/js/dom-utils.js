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
