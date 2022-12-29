import { postTelemetryData } from "./apiClient";
import { loadToken } from "./auth";
import { getKey } from "./client-db";

export function sendData(element, value, points, token) {
  const slug = getKey(element);

  if (!token) {
    token = loadToken();
  }

  if (token && telemetryEnabled && backendUrl && courseSlug) {
    postTelemetryData(token, value, slug, extractTags(element), points);
  }
}

function extractTags(element) {
  const tags = [];
  const tagPrefix = "tag-";
  for (let className of element.classList) {
    if (className.startsWith(tagPrefix)) {
      tags.push(className.substring(tagPrefix.length));
    }
  }
  return tags;
}
