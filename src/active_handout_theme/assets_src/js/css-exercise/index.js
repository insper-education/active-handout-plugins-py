import { SandpackClient } from "@codesandbox/sandpack-client";
import { CodeJar } from "codejar";
import hljs from "highlight.js";
import {
  queryEditors,
  queryPlaygrounds,
  queryPreview,
  queryTabs,
} from "./queries";

function build_html_file(content) {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="/index.css">
</head>
<body>
${content}
<script src="/index.js">
</body>
</html>`;
}

export function initCSSPlugin(rememberCallbacks) {
  hljs.configure({
    languages: ["html", "js", "css"],
  });

  const playgrounds = queryPlaygrounds();
  playgrounds.forEach((playground) => {
    let sandpack;
    const files = {};
    const info = {
      files,
      entry: "/index.html",
      dependencies: {
        uuid: "latest",
      },
    };

    const tabs = queryTabs(playground);
    const editors = queryEditors(playground);
    editors.forEach((editor) => {
      const filename = editor.getAttribute("data-filename");
      let content = editor.textContent;
      if (filename.endsWith("html")) {
        content = build_html_file(content);
      }

      files[filename] = { code: content };

      const jar = CodeJar(editor, hljs.highlightElement);
      jar.onUpdate((code) => {
        if (filename.endsWith("html")) {
          code = build_html_file(code);
        }
        files[filename].code = code;
        sandpack.updatePreview(info);
      });
    });

    setupTabs(tabs, editors);

    sandpack = new SandpackClient(queryPreview(playground), info, {
      showOpenInCodeSandbox: false,
    });
  });
}

function setupTabs(tabs, editors) {
  tabs.forEach((tab, idx) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      editors.forEach((e, editorIdx) => {
        if (editorIdx === idx) {
          e.classList.add("active");
        } else e.classList.remove("active");
      });
    });
  });
}
