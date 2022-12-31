import { buildUrl } from "../apiClient";
import { createElementWithClasses } from "../dom-utils";

export async function loadDashboard(container, userInfo, token, tagTree) {
  if (!courseSlug) {
    return;
  }

  const safeTagTree = encodeURI(JSON.stringify(tagTree));
  const safeCourseSlug = encodeURI(courseSlug);
  const endpoint = `../dashboard/${safeCourseSlug}/student/${userInfo.id}?tag-tree=${safeTagTree}`;
  const iframe = createElementWithClasses(
    "iframe",
    ["ah-dashboard"],
    container
  );

  let prevHeight = 0;
  window.addEventListener(
    "message",
    (event) => {
      if (!backendUrl || !backendUrl.includes(event.origin)) {
        return;
      }

      var { event: receivedEvent, height: iframeHeight } = JSON.parse(
        event.data
      );

      if (receivedEvent !== "resize") {
        return;
      }

      // A few extra pixels to make sure there will be no scrollbar
      const extra = 10;
      const newHeight = iframeHeight + extra;
      if (prevHeight !== newHeight - extra) {
        iframe.style.height = newHeight + "px";
        prevHeight = newHeight;
      }
    },
    false
  );

  iframe.src = buildUrl(endpoint);
}
