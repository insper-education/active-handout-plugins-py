import { loadUserInfo } from "../auth";

export function initDashboard() {
  if (!dashboardEnabled) return;

  const container = document.querySelector(".dashboard-container");
  if (!container) return;

  // container.setAttribute("hx-post", "");
  // container.setAttribute("hx-trigger", "load");
  const userInfo = loadUserInfo();
  if (!userInfo) {
    console.error(
      "No user info found. Container was found, but dashboard can't loaded."
    );
    return;
  }

  if (!tagTree) {
    console.error(
      "No tag tree found. Container was found, but dashboard can't loaded."
    );
    return;
  }

  const safeTagTree = JSON.stringify(tagTree);
  const unencodedUrl = `${dashboardUrl}${userInfo.id}?tag-tree=${safeTagTree}`;
  const url = encodeURI(unencodedUrl);
  console.log(url);
}
