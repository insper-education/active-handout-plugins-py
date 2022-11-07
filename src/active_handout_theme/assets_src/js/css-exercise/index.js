import { SandpackClient } from "@codesandbox/sandpack-client";
import { CodeJar } from "codejar";
import hljs from "highlight.js";
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
  queryTestButtonFromExercise,
  queryTestButtonFromPlayground,
} from "./queries";
import { allEqualRects, deepCopy } from "./dom-utils";
import { initFiles } from "./files";

const allRects = {};

export function initCSSPlugin(rememberCallbacks) {
  initHljs();
  initComputedRectsMessageListener();

  const playgrounds = queryPlaygrounds();
  playgrounds.forEach(initPlayground);
}

function initPlayground(playground) {
  const editors = queryEditors(playground);
  const tabs = queryTabs(playground);
  const exercise = queryExerciseFromPlayground(playground);
  const resetButton = queryResetButtonFromPlayground(playground);
  const testButton = queryTestButtonFromPlayground(playground);

  const files = initFiles(editors);
  const origFiles = deepCopy(files);
  const updateSandpack = initSandpack(queryPreview(playground), files);

  const codeJars = Object.fromEntries(
    Array.from(editors).map(buildInitCodeJar(exercise, files, updateSandpack))
  );

  resetButton.addEventListener(
    "click",
    buildResetClickListener(
      playground,
      files,
      origFiles,
      codeJars,
      updateSandpack
    )
  );

  testButton.addEventListener("click", buildTestClickListener(playground));

  setupTabs(tabs, editors);
  buildExpectedResult(playground, files);
}

function initSandpack(iframe, files) {
  const info = {
    files,
    entry: "/main.js",
    dependencies: {
      uuid: "latest",
    },
  };
  const sandpack = new SandpackClient(iframe, info, {
    showOpenInCodeSandbox: false,
  });

  function updateSandpack() {
    sandpack.updatePreview(info);
  }

  return updateSandpack;
}

function buildInitCodeJar(exercise, files, updateSandpack) {
  return (editor) => {
    const filename = editor.getAttribute("data-filename");

    const jar = CodeJar(editor, hljs.highlightElement);
    jar.onUpdate(
      buildCodeUpdateListener(exercise, files[filename], updateSandpack)
    );

    return [filename, jar];
  };
}

function initHljs() {
  hljs.configure({
    languages: ["html", "js", "css"],
  });
}

function initComputedRectsMessageListener() {
  window.addEventListener("message", (event) => {
    if (event.data?.message !== "computeRects") return;

    const { exerciseId, origin, rects } = event.data;
    allRects[exerciseId][origin] = rects;

    const { preview, expected } = allRects[exerciseId];
    if (preview && expected) {
      const exercise = document.getElementById(exerciseId);
      if (allEqualRects(preview, expected)) {
        // TODO: TELEMETRY
        exercise.classList.add("done");
        const testButton = queryTestButtonFromExercise(exercise);
        testButton.disabled = true;
      } else {
        exercise.classList.add("wrong");
      }
    }
  });
}

function buildCodeUpdateListener(exercise, file, updateSandpack) {
  const testButton = queryTestButtonFromExercise(exercise);

  return (code) => {
    file.code = code;
    updateSandpack();
    resetExercise(exercise);
    testButton.disabled = false;
  };
}

function buildResetClickListener(
  playground,
  files,
  origFiles,
  codeJars,
  updateSandpack
) {
  const exercise = queryExerciseFromPlayground(playground);
  const testButton = queryTestButtonFromPlayground(playground);

  return () => {
    resetExercise(exercise);
    testButton.disabled = false;

    for (let filename in origFiles) {
      const code = origFiles[filename].code;
      files[filename].code = code;
      const jar = codeJars[filename];
      jar?.updateCode(code);
      updateSandpack();
    }
  };
}

function buildTestClickListener(playground) {
  return () => {
    const exercise = queryExerciseFromPlayground(playground);
    const previewIframe = queryPreview(playground);
    const expectedIframe = queryExpectedResult(playground);

    resetExercise(exercise);

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
  };
}

function resetExercise(exercise) {
  exercise.classList.remove("done");
  exercise.classList.remove("wrong");
}

function buildExpectedResult(playground, files) {
  files = deepCopy(files);

  const answer = queryAnswerFromPlayground(playground);
  const answerFiles = queryAnswerFiles(answer);

  answerFiles.forEach((answerFile) => {
    const filename = extractFilename(answerFile);
    files[filename].code = answerFile.textContent;
  });

  initSandpack(queryExpectedResult(playground), files);
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
