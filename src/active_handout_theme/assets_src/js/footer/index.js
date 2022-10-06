export function initFooterPlugin() {
  const contentRect = document
    .getElementsByClassName("ah-content")[0]
    .getBoundingClientRect();
  const baseRight = contentRect.right;
  const baseTop = contentRect.top;
  const footnoteLinks = document.getElementsByClassName("footnote-ref");
  for (let footnoteLink of footnoteLinks) {
    const footnoteRef = footnoteLink.closest("sup").previousElementSibling;
    const noteId = footnoteLink.getAttribute("href").substring(1);
    const note = document.getElementById(noteId);
    const rect = footnoteRef.getBoundingClientRect();
    const distX = baseRight - rect.left;
    const refY = rect.bottom - baseTop;
    console.log(baseTop, rect.bottom);

    note.classList.add("floating-note");
    note.style.setProperty("--dist-x", `${distX}px`);
    note.style.setProperty("--ref-y", `${refY}px`);
  }
}
