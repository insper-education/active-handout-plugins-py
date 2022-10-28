import { SandpackClient } from "@codesandbox/sandpack-client";
import { CodeJar } from "codejar";
import hljs from "highlight.js";
import { queryEditors, queryPlaygrounds } from "./queries";

export function initCSSPlugin(rememberCallbacks) {
  hljs.configure({
    languages: ["html", "js", "css"],
  });

  const playgrounds = queryPlaygrounds();
  playgrounds.forEach((playground) => {
    const editors = queryEditors(playground);
    editors.forEach((editor) => {
      const jar = CodeJar(editor, hljs.highlightElement);
    });

    const sandpack = new SandpackClient(
      playground,
      {
        files: {
          "/index.html": {
            code: `<script src="./index.js"></script><div><p>Blabla</p></div>`,
          },
          "/index.js": {
            code: `console.log(require('uuid'))`,
          },
        },
        entry: "/index.js",
        dependencies: {
          uuid: "latest",
        },
      },
      { showOpenInCodeSandbox: false }
    );
  });
}
