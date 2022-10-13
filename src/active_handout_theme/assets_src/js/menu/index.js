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

  document.addEventListener("click", (event) => {
    console.log(
      window.innerWidth,
      getBreakpoint("medium"),
      window.innerWidth > getBreakpoint("medium")
    );
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
