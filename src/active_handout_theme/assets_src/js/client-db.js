function getKey(elOrKey) {
  if (typeof elOrKey === "string") {
    return elOrKey;
  }
  const docAddr = document.location.pathname;
  return `${docAddr}/${elOrKey.id}`;
}

export function setValue(elOrKey, value) {
  const key = getKey(elOrKey);
  localStorage[key] = value;
}

export function getValue(elOrKey) {
  const key = getKey(elOrKey);
  return localStorage.getItem(key);
}
