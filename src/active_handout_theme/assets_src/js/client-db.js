function getKey(elOrKey) {
  if (typeof elOrKey === "string") {
    return elOrKey;
  }
  const docAddr = document.location.pathname;
  const slash = docAddr.endsWith("/") ? "" : "/";
  return `${docAddr}${slash}${elOrKey.id}`;
}

export function setValue(elOrKey, value) {
  const key = getKey(elOrKey);
  localStorage[key] = value;
}

export function getValue(elOrKey) {
  const key = getKey(elOrKey);
  return localStorage.getItem(key);
}

export function removeValue(elOrKey) {
    const key = getKey(elOrKey);
    localStorage.removeItem(key);
