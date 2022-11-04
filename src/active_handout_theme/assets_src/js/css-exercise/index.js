import { SandpackClient } from "@codesandbox/sandpack-client";
import { CodeJar } from "codejar";
import hljs from "highlight.js";
import { approximatelyEqual, deepCopy } from "../dom-utils";
import {
  extractFilename,
  queryAnswerFiles,
  queryAnswerFromPlayground,
  queryEditors,
  queryExerciseFromPlayground,
  queryExpectedResult,
  queryPlaygrounds,
  queryPreview,
  queryResetButtonFromPlayground,
  queryTabs,
  queryTestButtonFromPlayground,
} from "./queries";

function build_html_file(content) {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=300, height=200, initial-scale=1", user-scalable="no">
</head>
<body>
${content}
</body>
</html>`;
}

function build_main_js(files) {
  mainjs = "";
  for (let filename in files) {
    if (!filename.endsWith("html")) {
      mainjs += `import "/${filename}";\n`;
    }
  }
  return mainjs;
}

function initFiles() {
  return {
    "reset.css": {
      code: `
/* http://meyerweb.com/eric/tools/css/reset/
   v2.0 | 20110126
   License: none (public domain)
*/
html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed,
figure, figcaption, footer, header, hgroup,
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}
/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure,
footer, header, hgroup, menu, nav, section {
  display: block;
}
body {
  line-height: 1;
}
ol, ul {
  list-style: none;
}
blockquote, q {
  quotes: none;
}
blockquote:before, blockquote:after,
q:before, q:after {
  content: '';
  content: none;
}
table {
  border-collapse: collapse;
  border-spacing: 0;
}
/* Active Handout custom iframe reset */
body {
  width: 100vw;
  height: 100vh;
  margin: 0 auto;
  padding: 0;
  font-family: sans-serif;
  overflow: hidden;
}
`,
    },
    "css-exercise.js": {
      code: `
function listAllElements(parent) {
  let elements = [];
  for (let child of parent.childNodes) {
    if (child.nodeType === Node.ELEMENT_NODE) {
      elements.push(child);
      elements = elements.concat(listAllElements(child));
    }
  }
  return elements;
}

function getRect(element) {
  const rect = element.getBoundingClientRect();
  return {x: rect.x, y: rect.y, width: rect.width, height: rect.height};
}

window.addEventListener("message", function(event) {
  if (event.data?.message !== "computeRects") return;

  const elements = listAllElements(document.querySelector("body"));
  const rects = elements.map(getRect);

  event.data.rects = rects;

  event.source.postMessage(event.data, "*");
});
`,
    },
  };
}

function allEqualRects(preview, expected) {
  if (preview.length !== expected.length) return false;

  for (let i = 0; i < preview.length; i++) {
    for (let attr of ["x", "y", "width", "height"]) {
      if (!approximatelyEqual(preview[i][attr], expected[i][attr], 5))
        return false;
    }
  }

  return true;
}

const allRects = {};
export function initCSSPlugin(rememberCallbacks) {
  hljs.configure({
    languages: ["html", "js", "css"],
  });

  window.addEventListener("message", (event) => {
    if (event.data?.message !== "computeRects") return;

    const { exerciseId, origin, rects } = event.data;
    allRects[exerciseId][origin] = rects;

    const { preview, expected } = allRects[exerciseId];
    if (preview && expected) {
      const exercise = document.getElementById(exerciseId);
      if (allEqualRects(preview, expected)) {
        // TODO: TELEMETRY
        // TODO: (STOPPED HERE) DISABLE EDITORS AND TEST BUTTON
        exercise.classList.add("done");
      } else {
        exercise.classList.add("wrong");
      }
    }
  });

  const playgrounds = queryPlaygrounds();
  playgrounds.forEach((playground) => {
    let sandpack;
    const files = initFiles();
    const info = {
      files,
      entry: "/main.js",
      dependencies: {
        uuid: "latest",
      },
    };

    const tabs = queryTabs(playground);
    const editors = queryEditors(playground);
    const codeJars = {};
    editors.forEach((editor) => {
      const filename = editor.getAttribute("data-filename");
      let content = editor.textContent;
      if (filename.endsWith("html")) {
        content = build_html_file(content);
      }

      files[filename] = { code: content };

      const jar = CodeJar(editor, hljs.highlightElement);
      codeJars[filename] = jar;
      jar.onUpdate((code) => {
        if (filename.endsWith("html")) {
          code = build_html_file(code);
        }
        files[filename].code = code;
        sandpack.updatePreview(info);
      });
    });
    files["main.js"] = { code: build_main_js(files) };

    const origFiles = deepCopy(files);
    const resetButton = queryResetButtonFromPlayground(playground);
    resetButton.addEventListener("click", () => {
      const exercise = queryExerciseFromPlayground(playground);
      exercise.classList.remove("done");
      exercise.classList.remove("wrong");

      for (let filename in origFiles) {
        const code = origFiles[filename].code;
        files[filename].code = code;
        const jar = codeJars[filename];
        jar?.updateCode(code);
        sandpack.updatePreview(info);
      }
    });

    const testButton = queryTestButtonFromPlayground(playground);
    testButton.addEventListener("click", () => {
      const exercise = queryExerciseFromPlayground(playground);
      const previewIframe = queryPreview(playground);
      const expectedIframe = queryExpectedResult(playground);

      exercise.classList.remove("done");
      exercise.classList.remove("wrong");

      allRects[exercise.id] = {};

      previewIframe.contentWindow.postMessage(
        {
          message: "computeRects",
          origin: "preview",
          exerciseId: exercise.id,
        },
        "*"
      );
      expectedIframe.contentWindow.postMessage(
        {
          message: "computeRects",
          origin: "expected",
          exerciseId: exercise.id,
        },
        "*"
      );
    });

    setupTabs(tabs, editors);

    sandpack = new SandpackClient(queryPreview(playground), info, {
      showOpenInCodeSandbox: false,
    });
    buildExpectedResult(playground, info);
  });
}

function buildExpectedResult(playground, info) {
  const expectedResultInfo = deepCopy(info);

  const answer = queryAnswerFromPlayground(playground);
  const answerFiles = queryAnswerFiles(answer);
  answerFiles.forEach((answerFile) => {
    const filename = extractFilename(answerFile);
    expectedResultInfo.files[filename].code = answerFile.textContent;
  });

  new SandpackClient(queryExpectedResult(playground), expectedResultInfo, {
    showOpenInCodeSandbox: false,
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
