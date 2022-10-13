import { setValue } from "../client-db";
import { getBreakpoint } from "../breakpoints";

function isMenuOpened(menuBtn) {
  return menuBtn.getAttribute("data-action") === "close";
}

export function initMenuPlugin(rememberCallbacks) {
  const btnClass = "ah-menu-btn";
  const navClass = "ah-navigation";

  rememberCallbacks.push({
    match: (el) => el.classList.contains(btnClass),
    callback: (el) => {
      setValue("menu-opened", isMenuOpened(el));
    },
  });

  const nav = document.getElementsByClassName(navClass)[0];
  const navContainer = nav.getElementsByClassName("ah-nav-container")[0];
  const menuBtns = document.getElementsByClassName(btnClass);
  for (let menuBtn of menuBtns) {
    menuBtn.addEventListener("click", function (event) {
      event.stopPropagation();
      if (isMenuOpened(menuBtn)) {
        nav.classList.remove("show");
      } else {
        nav.classList.add("show");
      }
    });
  }

  const togglableItems = document.getElementsByClassName("ah-togglable-item");
  for (let item of togglableItems) {
    const handle = item.getElementsByClassName("ah-togglable-handle")[0];
    handle.addEventListener("click", function (event) {
      event.stopPropagation();
      item.classList.toggle("opened");
    });
  }

  document.addEventListener("click", function (event) {
    if (
      !nav.classList.contains("show") ||
      window.innerWidth > getBreakpoint("medium")
    )
      return;
    if (!navContainer.contains(event.target)) {
      nav.classList.remove("show");
    }
  });
}
