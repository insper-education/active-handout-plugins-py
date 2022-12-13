import { CodeJar } from "codejar";
import hljs from "highlight.js";
import { deepCopy } from "../dom-utils";
import { initFiles } from "./files";
import { queryEditors, queryFileContents, queryFileTabs } from "./queries";
import { createReadonlyCodeJar } from "./readonly-codejar";

export function initCodeEditorPlugin() {
  const editors = queryEditors();
  editors.forEach(initEditor);
}

function initEditor(editor) {
  const fileContents = Array.from(queryFileContents(editor));
  const tabs = queryFileTabs(editor);

  const files = initFiles(fileContents);

  fileContents.forEach(buildInitSubEditor(editor, files));

  setupTabs(tabs, editor);
}

function buildInitSubEditor(editor, files) {
  // TODO: add reset button
  const origFiles = deepCopy(files);

  return (fileContent) => {
    const filename = fileContent.getAttribute("data-filename");
    const readonly = fileContent.getAttribute("data-readonly") === "true";
    const language = fileContent.getAttribute("data-language");
    const code = files[filename].code;

    let jar;
    if (readonly) {
      jar = createReadonlyCodeJar(fileContent, code);
    } else {
      jar = CodeJar(fileContent, (element) => {
        if (language) {
          hljs.configure({
            languages: [language],
          });
        }
        hljs.highlightElement(element);
      });
      jar.onUpdate((code) => {
        files[filename].code = code;

        // Dispatch event so others can do whatever they want with the new code
        const event = new CustomEvent("contentchanged", {
          detail: { filename, code },
        });
        editor.dispatchEvent(event);
      });
      jar.updateCode(code);
    }

    return [filename, jar];
  };
}

function setupTabs(tabs, editor) {
  tabs.forEach((tab, idx) => {
    tab.addEventListener("click", () => {
      editor.style.setProperty("--current-file", idx);

      tabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
    });
  });
}
