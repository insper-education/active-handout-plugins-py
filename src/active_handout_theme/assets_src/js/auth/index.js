const USER_DATA_KEY = "active-handout--user-data";

export function loadUser() {
  return localStorage.getItem(USER_DATA_KEY);
}

export function initAuth() {
  handleRedirects();
  let user = loadUser();

  const authMenuContainer = document.getElementById("user-menu");
  document.body.addEventListener("htmx:afterSettle", function (evt) {
    if (evt.target == authMenuContainer) {
      if (user) {
        document.getElementById("logout_btn").classList.remove("hidden");
      } else {
        document.getElementById("login_btn").classList.remove("hidden");
      }
    }
  });

  return user;
}

function handleRedirects() {
  if (location.search.includes("token=")) {
    const params = new URLSearchParams(location.search);
    const token = params.get("token");
    localStorage.setItem(USER_DATA_KEY, token);
    window.location.href = window.location.href.replace(
      window.location.search,
      ""
    );
  }
}
