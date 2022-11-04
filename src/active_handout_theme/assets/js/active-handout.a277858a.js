// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles

(function (modules, entry, mainEntry, parcelRequireName, globalName) {
  /* eslint-disable no-undef */
  var globalObject =
    typeof globalThis !== 'undefined'
      ? globalThis
      : typeof self !== 'undefined'
      ? self
      : typeof window !== 'undefined'
      ? window
      : typeof global !== 'undefined'
      ? global
      : {};
  /* eslint-enable no-undef */

  // Save the require from previous bundle to this closure if any
  var previousRequire =
    typeof globalObject[parcelRequireName] === 'function' &&
    globalObject[parcelRequireName];

  var cache = previousRequire.cache || {};
  // Do not use `require` to prevent Webpack from trying to bundle this call
  var nodeRequire =
    typeof module !== 'undefined' &&
    typeof module.require === 'function' &&
    module.require.bind(module);

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire =
          typeof globalObject[parcelRequireName] === 'function' &&
          globalObject[parcelRequireName];
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error("Cannot find module '" + name + "'");
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = (cache[name] = new newRequire.Module(name));

      modules[name][0].call(
        module.exports,
        localRequire,
        module,
        module.exports,
        this
      );
    }

    return cache[name].exports;

    function localRequire(x) {
      var res = localRequire.resolve(x);
      return res === false ? {} : newRequire(res);
    }

    function resolve(x) {
      var id = modules[name][1][x];
      return id != null ? id : x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [
      function (require, module) {
        module.exports = exports;
      },
      {},
    ];
  };

  Object.defineProperty(newRequire, 'root', {
    get: function () {
      return globalObject[parcelRequireName];
    },
  });

  globalObject[parcelRequireName] = newRequire;

  for (var i = 0; i < entry.length; i++) {
    newRequire(entry[i]);
  }

  if (mainEntry) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(mainEntry);

    // CommonJS
    if (typeof exports === 'object' && typeof module !== 'undefined') {
      module.exports = mainExports;

      // RequireJS
    } else if (typeof define === 'function' && define.amd) {
      define(function () {
        return mainExports;
      });

      // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }
})({"ecP4v":[function(require,module,exports) {
var _tabbedContent = require("./tabbed-content");
var _progress = require("./progress");
var _question = require("./question");
document.addEventListener("DOMContentLoaded", function() {
    console.log("ASDDSAAHERHASD");
    (0, _tabbedContent.initTabbedPlugin)();
    let rememberCallbacks = [];
    (0, _progress.initProgressPlugin)(rememberCallbacks);
    (0, _question.initQuestionPlugin)(rememberCallbacks);
    window.addEventListener("remember", function(e) {
        const element = e.detail.element;
        for (let remember of rememberCallbacks)if (remember.match(element)) {
            remember.callback(element);
            break;
        }
    });
});

},{"./progress":"fzxNo","./question":"132rX","./tabbed-content":"eIlmk"}],"fzxNo":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "initProgressPlugin", ()=>initProgressPlugin);
var _clientDb = require("../client-db");
var _telemetry = require("../telemetry");
function initProgressPlugin(rememberCallbacks) {
    queryProgressBtns().forEach((e)=>{
        if ((0, _clientDb.getValue)(e)) e.click();
    });
    rememberCallbacks.push({
        match: (el)=>el.classList.contains("progress"),
        callback: (el)=>{
            (0, _telemetry.saveAndSendData)(el, true);
        }
    });
}
function queryProgressBtns() {
    return document.querySelectorAll("button.progress");
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"5oERU","../telemetry":"kpvgZ","../client-db":"j0pff"}],"5oERU":[function(require,module,exports) {
exports.interopDefault = function(a) {
    return a && a.__esModule ? a : {
        default: a
    };
};
exports.defineInteropFlag = function(a) {
    Object.defineProperty(a, "__esModule", {
        value: true
    });
};
exports.exportAll = function(source, dest) {
    Object.keys(source).forEach(function(key) {
        if (key === "default" || key === "__esModule" || dest.hasOwnProperty(key)) return;
        Object.defineProperty(dest, key, {
            enumerable: true,
            get: function() {
                return source[key];
            }
        });
    });
    return dest;
};
exports.export = function(dest, destName, get) {
    Object.defineProperty(dest, destName, {
        enumerable: true,
        get: get
    });
};

},{}],"kpvgZ":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "saveAndSendData", ()=>saveAndSendData);
var _clientDb = require("./client-db");
function saveAndSendData(elOrKey, value) {
    (0, _clientDb.setValue)(elOrKey, value);
    let dataCollectionURL = "{{ config.extra.telemetry_url }}";
// TODO: fetch POST with token
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"5oERU","./client-db":"j0pff"}],"j0pff":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "setValue", ()=>setValue);
parcelHelpers.export(exports, "getValue", ()=>getValue);
function getKey(elOrKey) {
    if (typeof elOrKey === "string") return elOrKey;
    const docAddr = document.location.pathname;
    return `${docAddr}/${elOrKey.id}`;
}
function setValue(elOrKey, value) {
    const key = getKey(elOrKey);
    localStorage[key] = value;
}
function getValue(elOrKey) {
    const key = getKey(elOrKey);
    return localStorage.getItem(key);
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"5oERU"}],"132rX":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "initQuestionPlugin", ()=>initQuestionPlugin);
var _clientDb = require("../client-db");
var _telemetry = require("../telemetry");
var _queries = require("./queries");
function initQuestionPlugin(rememberCallbacks) {
    initTextQuestions(rememberCallbacks);
    initChoiceQuestions(rememberCallbacks);
    initExercises(rememberCallbacks);
}
function initTextQuestions(rememberCallbacks) {
    (0, _queries.queryTextQuestions)().forEach((el)=>{
        const prevAnswer = (0, _clientDb.getValue)(el);
        if (prevAnswer !== null) {
            (0, _queries.queryTextInputs)(el).value = prevAnswer;
            (0, _queries.querySubmitBtn)(el).click();
        }
    });
    rememberCallbacks.push({
        match: (el)=>el.classList.contains("short") || el.classList.contains("medium") || el.classList.contains("long"),
        callback: (el)=>{
            const textElement = (0, _queries.queryTextInputs)(el);
            (0, _telemetry.saveAndSendData)(element, textElement.value);
        }
    });
}
function initChoiceQuestions(rememberCallbacks) {
    (0, _queries.queryChoiceQuestions)().forEach((el)=>{
        const prevAnswer = (0, _clientDb.getValue)(el);
        if (prevAnswer !== null) {
            (0, _queries.queryOption)(el, prevAnswer).checked = true;
            (0, _queries.querySubmitBtn)(el).click();
        }
    });
    rememberCallbacks.push({
        match: (el)=>el.classList.contains("choice"),
        callback: (el)=>{
            const choices = (0, _queries.queryOptions)(el);
            for (let choice of choices)if (choice.checked) (0, _telemetry.saveAndSendData)(el, choice.value);
        }
    });
}
function initExercises(rememberCallbacks) {
    (0, _queries.queryExercises)().forEach((el)=>{
        const prevAnswer = (0, _clientDb.getValue)(el);
        if (prevAnswer !== null) (0, _queries.querySubmitBtn)(el).click();
    });
    rememberCallbacks.push({
        match: (el)=>el.classList.contains("exercise"),
        callback: (el)=>{
            (0, _telemetry.saveAndSendData)(el, true);
        }
    });
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"5oERU","./queries":"jbGr6","../client-db":"j0pff","../telemetry":"kpvgZ"}],"jbGr6":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "queryTextQuestions", ()=>queryTextQuestions);
parcelHelpers.export(exports, "queryChoiceQuestions", ()=>queryChoiceQuestions);
parcelHelpers.export(exports, "queryExercises", ()=>queryExercises);
parcelHelpers.export(exports, "queryTextInputs", ()=>queryTextInputs);
parcelHelpers.export(exports, "queryOptions", ()=>queryOptions);
parcelHelpers.export(exports, "queryOption", ()=>queryOption);
parcelHelpers.export(exports, "querySubmitBtn", ()=>querySubmitBtn);
function queryTextQuestions() {
    return document.querySelectorAll("div.admonition.question.short, div.admonition.question.medium, div.admonition.question.long");
}
function queryChoiceQuestions() {
    return document.querySelectorAll("div.admonition.question.choice");
}
function queryExercises() {
    return document.querySelectorAll("div.admonition.exercise");
}
function queryTextInputs(el) {
    return el.querySelector("input[name='data'], textarea[name='data']");
}
function queryOptions(el) {
    return el.querySelectorAll("input[name='data'][type='radio']");
}
function queryOption(el, value) {
    return el.querySelector(`input[name='data'][value='${value}'`);
}
function querySubmitBtn(el) {
    return el.querySelector("input[type='submit']");
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"5oERU"}],"eIlmk":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "initTabbedPlugin", ()=>initTabbedPlugin);
// Source: https://facelessuser.github.io/pymdown-extensions/extensions/tabbed/
// Identify whether a tab bar can be scrolled left or right and apply indicator classes
const tabOverflow = ()=>{
    const checkScroll = (e)=>{
        // Use a margin as we just don't always align exactly on the right.
        const margin = 3;
        const target = e.target;
        if (!e.target.matches(".tabbed-labels")) return;
        const scrollWidth = target.scrollWidth - target.clientWidth;
        target.classList.remove("tabbed-scroll-left", "tabbed-scroll-right");
        if (e.type === "resize" || e.type === "scroll") {
            if (scrollWidth === 0) return;
            if (!target.scrollLeft) target.classList.add("tabbed-scroll-right");
            else if (target.scrollLeft < scrollWidth - margin) target.classList.add("tabbed-scroll-left", "tabbed-scroll-right");
            else target.classList.add("tabbed-scroll-left");
        }
    };
    // Change the tab to either the previous or next input - depending on which indicator was clicked.
    // Make sure the current, selected input is scrolled into view.
    const tabChange = (e)=>{
        const target = e.target;
        const selected = target.closest(".tabbed-set").querySelector("input:checked");
        let updated = null;
        if (target.classList.contains("tabbed-scroll-right") && e.offsetX >= e.target.offsetWidth - 15) {
            const sib = selected.nextSibling;
            updated = selected;
            if (sib && sib.tagName === "INPUT") updated = sib;
        } else if (target.classList.contains("tabbed-scroll-left") && e.offsetX <= 15) {
            const sib1 = selected.previousSibling;
            updated = selected;
            if (sib1 && sib1.tagName === "INPUT") updated = sib1;
        }
        if (updated) updated.click();
    };
    const onResize = new ResizeObserver((entries)=>{
        entries.forEach((entry)=>{
            checkScroll({
                target: entry.target,
                type: "resize"
            });
        });
    });
    const labels = document.querySelectorAll(".tabbed-alternate > .tabbed-labels");
    labels.forEach((el)=>{
        checkScroll({
            target: el,
            type: "resize"
        });
        onResize.observe(el);
        el.addEventListener("resize", checkScroll);
        el.addEventListener("scroll", checkScroll);
        el.addEventListener("click", tabChange);
    });
};
// Smooth scroll tab into view when changed
const tabScroll = ()=>{
    const tabs = document.querySelectorAll(".tabbed-alternate > input");
    for (const tab of tabs)tab.addEventListener("change", ()=>{
        const label = document.querySelector(`label[for=${tab.id}]`);
        label.scrollIntoView({
            block: "nearest",
            inline: "nearest",
            behavior: "smooth"
        });
    });
};
function initTabbedPlugin() {
    tabOverflow();
    tabScroll();
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"5oERU"}]},[], null, "parcelRequirea86e")

//# sourceMappingURL=active-handout.a277858a.js.map
