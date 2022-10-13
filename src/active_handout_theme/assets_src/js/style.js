export function initStyle() {
  const header = document.getElementsByClassName("ah-header")[0];
  document.documentElement.style.setProperty(
    "--header-height",
    `${header.offsetHeight}px`
  );
}
