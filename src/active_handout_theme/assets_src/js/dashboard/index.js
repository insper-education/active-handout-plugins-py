import { loadToken, loadUserInfo } from "../auth";
import { loadDashboard } from "./client";

export function initDashboard() {
  if (!dashboardEnabled) return;

  const container = document.querySelector(".dashboard-container");
  if (!container) return;

  const userInfo = loadUserInfo();
  const token = loadToken();
  if (!userInfo || !token) {
    console.error(
      "No user info or token found. Container was found, but dashboard can't loaded."
    );
    return;
  }

  if (!tagTree) {
    console.error(
      "No tag tree found. Container was found, but dashboard can't loaded."
    );
    return;
  }

  loadDashboard(container, userInfo, token, tagTree);
}
