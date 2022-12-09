import { postTelemetryData } from "./apiClient";
import { getKey, setValue } from "./client-db";

export function saveAndSendData(element, value, user, points) {
  const slug = getKey(element);
  setValue(slug, value);

  if (user && telemetryEnabled && backendUrl && courseSlug) {
    postTelemetryData(
      user,
      value,
      slug,
      extractTags(element),
      points
    );
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
