export function approximatelyEqual(a, b, epsilon) {
  if (!epsilon) epsilon = 0.1;
  return Math.abs(a - b) < epsilon;
}

export function allEqualRects(preview, expected) {
  if (preview.length !== expected.length) return false;

  for (let i = 0; i < preview.length; i++) {
    for (let attr of ["x", "y", "width", "height"]) {
      if (!approximatelyEqual(preview[i][attr], expected[i][attr], 5))
        return false;
    }
  }

  return true;
}

export function deepCopy(dict) {
  return JSON.parse(JSON.stringify(dict));
}
