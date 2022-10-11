import { setValue } from "../client-db";

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
  const menuBtns = document.getElementsByClassName(btnClass);
  for (let menuBtn of menuBtns) {
    menuBtn.addEventListener("click", function () {
      if (isMenuOpened(menuBtn)) {
        nav.classList.remove("show");
      } else {
        nav.classList.add("show");
      }
    });
  }
}
