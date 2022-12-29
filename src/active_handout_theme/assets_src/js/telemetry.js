import { postTelemetryData } from "./apiClient";
import { loadUser } from "./auth";
import { getKey } from "./client-db";

export function sendData(element, value, points, user) {
  const slug = getKey(element);

  if (!user) {
    user = loadUser();
  }

  if (user && telemetryEnabled && backendUrl && courseSlug) {
    postTelemetryData(user, value, slug, extractTags(element), points);
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
