export function initFiles(editors) {
  const files = {
    "reset.css": {
      code: RESET_CSS,
    },
    "css-exercise.js": {
      code: CSS_EXERCISE_JS,
    },
  };

  editors.forEach((editor) => {
    const filename = editor.getAttribute("data-filename");
    files[filename] = { code: editor.textContent };
  });

  files["main.js"] = { code: build_main_js(files) };

  return files;
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
  return { x: rect.x, y: rect.y, width: rect.width, height: rect.height };
}

function initCSSMessageListener() {
  window.addEventListener("message", function (event) {
    if (event.data?.message !== "computeRects") return;

    const elements = listAllElements(document.querySelector("body"));
    const rects = elements.map(getRect);

    event.data.rects = rects;

    event.source.postMessage(event.data, "*");
  });
}

const CSS_EXERCISE_JS = `
${listAllElements.toString()}
${getRect.toString()}
${initCSSMessageListener.toString()}

initCSSMessageListener()
`;

const RESET_CSS = `
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
`;
