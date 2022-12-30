import { getHTML } from "../apiClient";

export async function loadDashboard(container, userInfo, token, tagTree) {
  if (!courseSlug) {
    return;
  }

  const safeTagTree = encodeURI(JSON.stringify(tagTree));
  const safeCourseSlug = encodeURI(courseSlug);
  const endpoint = `../dashboard/fragments/${safeCourseSlug}/student/${userInfo.id}?tag-tree=${safeTagTree}`;
  getHTML(endpoint, token).then((html) => {
    if (!html) {
      container.innerHTML = "<p>Sorry, the dashboard couldn't be loaded...</p>";
    }
    container.innerHTML = html;
  });
}
