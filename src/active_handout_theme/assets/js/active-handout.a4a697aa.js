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
})({"1csOT":[function(require,module,exports) {
"use strict";
var global = arguments[3];
var HMR_HOST = null;
var HMR_PORT = 1234;
var HMR_SECURE = false;
var HMR_ENV_HASH = "916932b22e4085ab";
module.bundle.HMR_BUNDLE_ID = "efa96c9ba4a697aa";
/* global HMR_HOST, HMR_PORT, HMR_ENV_HASH, HMR_SECURE, chrome, browser, globalThis, __parcel__import__, __parcel__importScripts__, ServiceWorkerGlobalScope */ /*::
import type {
  HMRAsset,
  HMRMessage,
} from '@parcel/reporter-dev-server/src/HMRServer.js';
interface ParcelRequire {
  (string): mixed;
  cache: {|[string]: ParcelModule|};
  hotData: mixed;
  Module: any;
  parent: ?ParcelRequire;
  isParcelRequire: true;
  modules: {|[string]: [Function, {|[string]: string|}]|};
  HMR_BUNDLE_ID: string;
  root: ParcelRequire;
}
interface ParcelModule {
  hot: {|
    data: mixed,
    accept(cb: (Function) => void): void,
    dispose(cb: (mixed) => void): void,
    // accept(deps: Array<string> | string, cb: (Function) => void): void,
    // decline(): void,
    _acceptCallbacks: Array<(Function) => void>,
    _disposeCallbacks: Array<(mixed) => void>,
  |};
}
interface ExtensionContext {
  runtime: {|
    reload(): void,
    getURL(url: string): string;
    getManifest(): {manifest_version: number, ...};
  |};
}
declare var module: {bundle: ParcelRequire, ...};
declare var HMR_HOST: string;
declare var HMR_PORT: string;
declare var HMR_ENV_HASH: string;
declare var HMR_SECURE: boolean;
declare var chrome: ExtensionContext;
declare var browser: ExtensionContext;
declare var __parcel__import__: (string) => Promise<void>;
declare var __parcel__importScripts__: (string) => Promise<void>;
declare var globalThis: typeof self;
declare var ServiceWorkerGlobalScope: Object;
*/ var OVERLAY_ID = "__parcel__error__overlay__";
var OldModule = module.bundle.Module;
function Module(moduleName) {
    OldModule.call(this, moduleName);
    this.hot = {
        data: module.bundle.hotData,
        _acceptCallbacks: [],
        _disposeCallbacks: [],
        accept: function(fn) {
            this._acceptCallbacks.push(fn || function() {});
        },
        dispose: function(fn) {
            this._disposeCallbacks.push(fn);
        }
    };
    module.bundle.hotData = undefined;
}
module.bundle.Module = Module;
var checkedAssets, acceptedAssets, assetsToAccept /*: Array<[ParcelRequire, string]> */ ;
function getHostname() {
    return HMR_HOST || (location.protocol.indexOf("http") === 0 ? location.hostname : "localhost");
}
function getPort() {
    return HMR_PORT || location.port;
} // eslint-disable-next-line no-redeclare
var parent = module.bundle.parent;
if ((!parent || !parent.isParcelRequire) && typeof WebSocket !== "undefined") {
    var hostname = getHostname();
    var port = getPort();
    var protocol = HMR_SECURE || location.protocol == "https:" && !/localhost|127.0.0.1|0.0.0.0/.test(hostname) ? "wss" : "ws";
    var ws = new WebSocket(protocol + "://" + hostname + (port ? ":" + port : "") + "/"); // Web extension context
    var extCtx = typeof chrome === "undefined" ? typeof browser === "undefined" ? null : browser : chrome; // Safari doesn't support sourceURL in error stacks.
    // eval may also be disabled via CSP, so do a quick check.
    var supportsSourceURL = false;
    try {
        (0, eval)('throw new Error("test"); //# sourceURL=test.js');
    } catch (err) {
        supportsSourceURL = err.stack.includes("test.js");
    } // $FlowFixMe
    ws.onmessage = async function(event) {
        checkedAssets = {} /*: {|[string]: boolean|} */ ;
        acceptedAssets = {} /*: {|[string]: boolean|} */ ;
        assetsToAccept = [];
        var data = JSON.parse(event.data);
        if (data.type === "update") {
            // Remove error overlay if there is one
            if (typeof document !== "undefined") removeErrorOverlay();
            let assets = data.assets.filter((asset)=>asset.envHash === HMR_ENV_HASH); // Handle HMR Update
            let handled = assets.every((asset)=>{
                return asset.type === "css" || asset.type === "js" && hmrAcceptCheck(module.bundle.root, asset.id, asset.depsByBundle);
            });
            if (handled) {
                console.clear(); // Dispatch custom event so other runtimes (e.g React Refresh) are aware.
                if (typeof window !== "undefined" && typeof CustomEvent !== "undefined") window.dispatchEvent(new CustomEvent("parcelhmraccept"));
                await hmrApplyUpdates(assets);
                for(var i = 0; i < assetsToAccept.length; i++){
                    var id = assetsToAccept[i][1];
                    if (!acceptedAssets[id]) hmrAcceptRun(assetsToAccept[i][0], id);
                }
            } else fullReload();
        }
        if (data.type === "error") {
            // Log parcel errors to console
            for (let ansiDiagnostic of data.diagnostics.ansi){
                let stack = ansiDiagnostic.codeframe ? ansiDiagnostic.codeframe : ansiDiagnostic.stack;
                console.error("\uD83D\uDEA8 [parcel]: " + ansiDiagnostic.message + "\n" + stack + "\n\n" + ansiDiagnostic.hints.join("\n"));
            }
            if (typeof document !== "undefined") {
                // Render the fancy html overlay
                removeErrorOverlay();
                var overlay = createErrorOverlay(data.diagnostics.html); // $FlowFixMe
                document.body.appendChild(overlay);
            }
        }
    };
    ws.onerror = function(e) {
        console.error(e.message);
    };
    ws.onclose = function() {
        console.warn("[parcel] \uD83D\uDEA8 Connection to the HMR server was lost");
    };
}
function removeErrorOverlay() {
    var overlay = document.getElementById(OVERLAY_ID);
    if (overlay) {
        overlay.remove();
        console.log("[parcel] ✨ Error resolved");
    }
}
function createErrorOverlay(diagnostics) {
    var overlay = document.createElement("div");
    overlay.id = OVERLAY_ID;
    let errorHTML = '<div style="background: black; opacity: 0.85; font-size: 16px; color: white; position: fixed; height: 100%; width: 100%; top: 0px; left: 0px; padding: 30px; font-family: Menlo, Consolas, monospace; z-index: 9999;">';
    for (let diagnostic of diagnostics){
        let stack = diagnostic.frames.length ? diagnostic.frames.reduce((p, frame)=>{
            return `${p}
<a href="/__parcel_launch_editor?file=${encodeURIComponent(frame.location)}" style="text-decoration: underline; color: #888" onclick="fetch(this.href); return false">${frame.location}</a>
${frame.code}`;
        }, "") : diagnostic.stack;
        errorHTML += `
      <div>
        <div style="font-size: 18px; font-weight: bold; margin-top: 20px;">
          🚨 ${diagnostic.message}
        </div>
        <pre>${stack}</pre>
        <div>
          ${diagnostic.hints.map((hint)=>"<div>\uD83D\uDCA1 " + hint + "</div>").join("")}
        </div>
        ${diagnostic.documentation ? `<div>📝 <a style="color: violet" href="${diagnostic.documentation}" target="_blank">Learn more</a></div>` : ""}
      </div>
    `;
    }
    errorHTML += "</div>";
    overlay.innerHTML = errorHTML;
    return overlay;
}
function fullReload() {
    if ("reload" in location) location.reload();
    else if (extCtx && extCtx.runtime && extCtx.runtime.reload) extCtx.runtime.reload();
}
function getParents(bundle, id) /*: Array<[ParcelRequire, string]> */ {
    var modules = bundle.modules;
    if (!modules) return [];
    var parents = [];
    var k, d, dep;
    for(k in modules)for(d in modules[k][1]){
        dep = modules[k][1][d];
        if (dep === id || Array.isArray(dep) && dep[dep.length - 1] === id) parents.push([
            bundle,
            k
        ]);
    }
    if (bundle.parent) parents = parents.concat(getParents(bundle.parent, id));
    return parents;
}
function updateLink(link) {
    var newLink = link.cloneNode();
    newLink.onload = function() {
        if (link.parentNode !== null) // $FlowFixMe
        link.parentNode.removeChild(link);
    };
    newLink.setAttribute("href", link.getAttribute("href").split("?")[0] + "?" + Date.now()); // $FlowFixMe
    link.parentNode.insertBefore(newLink, link.nextSibling);
}
var cssTimeout = null;
function reloadCSS() {
    if (cssTimeout) return;
    cssTimeout = setTimeout(function() {
        var links = document.querySelectorAll('link[rel="stylesheet"]');
        for(var i = 0; i < links.length; i++){
            // $FlowFixMe[incompatible-type]
            var href = links[i].getAttribute("href");
            var hostname = getHostname();
            var servedFromHMRServer = hostname === "localhost" ? new RegExp("^(https?:\\/\\/(0.0.0.0|127.0.0.1)|localhost):" + getPort()).test(href) : href.indexOf(hostname + ":" + getPort());
            var absolute = /^https?:\/\//i.test(href) && href.indexOf(location.origin) !== 0 && !servedFromHMRServer;
            if (!absolute) updateLink(links[i]);
        }
        cssTimeout = null;
    }, 50);
}
function hmrDownload(asset) {
    if (asset.type === "js") {
        if (typeof document !== "undefined") {
            let script = document.createElement("script");
            script.src = asset.url + "?t=" + Date.now();
            if (asset.outputFormat === "esmodule") script.type = "module";
            return new Promise((resolve, reject)=>{
                var _document$head;
                script.onload = ()=>resolve(script);
                script.onerror = reject;
                (_document$head = document.head) === null || _document$head === void 0 || _document$head.appendChild(script);
            });
        } else if (typeof importScripts === "function") {
            // Worker scripts
            if (asset.outputFormat === "esmodule") return import(asset.url + "?t=" + Date.now());
            else return new Promise((resolve, reject)=>{
                try {
                    importScripts(asset.url + "?t=" + Date.now());
                    resolve();
                } catch (err) {
                    reject(err);
                }
            });
        }
    }
}
async function hmrApplyUpdates(assets) {
    global.parcelHotUpdate = Object.create(null);
    let scriptsToRemove;
    try {
        // If sourceURL comments aren't supported in eval, we need to load
        // the update from the dev server over HTTP so that stack traces
        // are correct in errors/logs. This is much slower than eval, so
        // we only do it if needed (currently just Safari).
        // https://bugs.webkit.org/show_bug.cgi?id=137297
        // This path is also taken if a CSP disallows eval.
        if (!supportsSourceURL) {
            let promises = assets.map((asset)=>{
                var _hmrDownload;
                return (_hmrDownload = hmrDownload(asset)) === null || _hmrDownload === void 0 ? void 0 : _hmrDownload.catch((err)=>{
                    // Web extension bugfix for Chromium
                    // https://bugs.chromium.org/p/chromium/issues/detail?id=1255412#c12
                    if (extCtx && extCtx.runtime && extCtx.runtime.getManifest().manifest_version == 3) {
                        if (typeof ServiceWorkerGlobalScope != "undefined" && global instanceof ServiceWorkerGlobalScope) {
                            extCtx.runtime.reload();
                            return;
                        }
                        asset.url = extCtx.runtime.getURL("/__parcel_hmr_proxy__?url=" + encodeURIComponent(asset.url + "?t=" + Date.now()));
                        return hmrDownload(asset);
                    }
                    throw err;
                });
            });
            scriptsToRemove = await Promise.all(promises);
        }
        assets.forEach(function(asset) {
            hmrApply(module.bundle.root, asset);
        });
    } finally{
        delete global.parcelHotUpdate;
        if (scriptsToRemove) scriptsToRemove.forEach((script)=>{
            if (script) {
                var _document$head2;
                (_document$head2 = document.head) === null || _document$head2 === void 0 || _document$head2.removeChild(script);
            }
        });
    }
}
function hmrApply(bundle, asset) {
    var modules = bundle.modules;
    if (!modules) return;
    if (asset.type === "css") reloadCSS();
    else if (asset.type === "js") {
        let deps = asset.depsByBundle[bundle.HMR_BUNDLE_ID];
        if (deps) {
            if (modules[asset.id]) {
                // Remove dependencies that are removed and will become orphaned.
                // This is necessary so that if the asset is added back again, the cache is gone, and we prevent a full page reload.
                let oldDeps = modules[asset.id][1];
                for(let dep in oldDeps)if (!deps[dep] || deps[dep] !== oldDeps[dep]) {
                    let id = oldDeps[dep];
                    let parents = getParents(module.bundle.root, id);
                    if (parents.length === 1) hmrDelete(module.bundle.root, id);
                }
            }
            if (supportsSourceURL) // Global eval. We would use `new Function` here but browser
            // support for source maps is better with eval.
            (0, eval)(asset.output);
             // $FlowFixMe
            let fn = global.parcelHotUpdate[asset.id];
            modules[asset.id] = [
                fn,
                deps
            ];
        } else if (bundle.parent) hmrApply(bundle.parent, asset);
    }
}
function hmrDelete(bundle, id) {
    let modules = bundle.modules;
    if (!modules) return;
    if (modules[id]) {
        // Collect dependencies that will become orphaned when this module is deleted.
        let deps = modules[id][1];
        let orphans = [];
        for(let dep in deps){
            let parents = getParents(module.bundle.root, deps[dep]);
            if (parents.length === 1) orphans.push(deps[dep]);
        } // Delete the module. This must be done before deleting dependencies in case of circular dependencies.
        delete modules[id];
        delete bundle.cache[id]; // Now delete the orphans.
        orphans.forEach((id)=>{
            hmrDelete(module.bundle.root, id);
        });
    } else if (bundle.parent) hmrDelete(bundle.parent, id);
}
function hmrAcceptCheck(bundle, id, depsByBundle) {
    if (hmrAcceptCheckOne(bundle, id, depsByBundle)) return true;
     // Traverse parents breadth first. All possible ancestries must accept the HMR update, or we'll reload.
    let parents = getParents(module.bundle.root, id);
    let accepted = false;
    while(parents.length > 0){
        let v = parents.shift();
        let a = hmrAcceptCheckOne(v[0], v[1], null);
        if (a) // If this parent accepts, stop traversing upward, but still consider siblings.
        accepted = true;
        else {
            // Otherwise, queue the parents in the next level upward.
            let p = getParents(module.bundle.root, v[1]);
            if (p.length === 0) {
                // If there are no parents, then we've reached an entry without accepting. Reload.
                accepted = false;
                break;
            }
            parents.push(...p);
        }
    }
    return accepted;
}
function hmrAcceptCheckOne(bundle, id, depsByBundle) {
    var modules = bundle.modules;
    if (!modules) return;
    if (depsByBundle && !depsByBundle[bundle.HMR_BUNDLE_ID]) {
        // If we reached the root bundle without finding where the asset should go,
        // there's nothing to do. Mark as "accepted" so we don't reload the page.
        if (!bundle.parent) return true;
        return hmrAcceptCheck(bundle.parent, id, depsByBundle);
    }
    if (checkedAssets[id]) return true;
    checkedAssets[id] = true;
    var cached = bundle.cache[id];
    assetsToAccept.push([
        bundle,
        id
    ]);
    if (!cached || cached.hot && cached.hot._acceptCallbacks.length) return true;
}
function hmrAcceptRun(bundle, id) {
    var cached = bundle.cache[id];
    bundle.hotData = {};
    if (cached && cached.hot) cached.hot.data = bundle.hotData;
    if (cached && cached.hot && cached.hot._disposeCallbacks.length) cached.hot._disposeCallbacks.forEach(function(cb) {
        cb(bundle.hotData);
    });
    delete bundle.cache[id];
    bundle(id);
    cached = bundle.cache[id];
    if (cached && cached.hot && cached.hot._acceptCallbacks.length) cached.hot._acceptCallbacks.forEach(function(cb) {
        var assetsToAlsoAccept = cb(function() {
            return getParents(module.bundle.root, id);
        });
        if (assetsToAlsoAccept && assetsToAccept.length) // $FlowFixMe[method-unbinding]
        assetsToAccept.push.apply(assetsToAccept, assetsToAlsoAccept);
    });
    acceptedAssets[id] = true;
}

},{}],"ecP4v":[function(require,module,exports) {
var _tabbedContent = require("./tabbed-content");
var _progress = require("./progress");
var _menu = require("./menu");
var _exercise = require("./exercise");
var _footnote = require("./footnote");
var _style = require("./style");
function onLoad() {
    (0, _tabbedContent.initTabbedPlugin)();
    let rememberCallbacks = [];
    window.addEventListener("remember", function(e) {
        const element = e.detail.element;
        for (let remember of rememberCallbacks)if (remember.match(element)) remember.callback(element);
    });
    (0, _style.initStyle)();
    (0, _menu.initMenuPlugin)();
    (0, _progress.initProgressPlugin)(rememberCallbacks);
    (0, _exercise.initExercisePlugin)(rememberCallbacks);
    (0, _footnote.initFooterPlugin)(rememberCallbacks);
}
if (document.readyState !== "loading") onLoad();
else document.addEventListener("DOMContentLoaded", onLoad);

},{"./progress":"fzxNo","./tabbed-content":"eIlmk","./exercise":"dmczC","./footnote":"70ehP","./menu":"5D3Be","./style":"5DGm5"}],"fzxNo":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "initProgressPlugin", ()=>initProgressPlugin);
var _clientDb = require("../client-db");
var _telemetry = require("../telemetry");
function initProgressPlugin(rememberCallbacks) {
    rememberCallbacks.push({
        match: (el)=>el.classList.contains("progress"),
        callback: (el)=>{
            (0, _telemetry.saveAndSendData)(el, true);
        }
    });
    queryProgressBtns().forEach((e)=>{
        if ((0, _clientDb.getValue)(e)) e.click();
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
    const slash = docAddr.endsWith("/") ? "" : "/";
    return `${docAddr}${slash}${elOrKey.id}`;
}
function setValue(elOrKey, value) {
    const key = getKey(elOrKey);
    localStorage[key] = value;
}
function getValue(elOrKey) {
    const key = getKey(elOrKey);
    return localStorage.getItem(key);
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
        target.classList.remove("tabbed-scroll", "tabbed-scroll-left", "tabbed-scroll-right");
        if (e.type === "resize" || e.type === "scroll") {
            if (scrollWidth === 0) return;
            target.classList.add("tabbed-scroll");
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

},{"@parcel/transformer-js/src/esmodule-helpers.js":"5oERU"}],"dmczC":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "initExercisePlugin", ()=>initExercisePlugin);
var _clientDb = require("../client-db");
var _telemetry = require("../telemetry");
var _queries = require("./queries");
function initExercisePlugin(rememberCallbacks) {
    rememberCallbacks.push({
        match: matchTextExercises,
        callback: rememberTextExercise
    }, {
        match: matchChoiceExercises,
        callback: rememberChoiceExercise
    }, {
        match: matchSelfProgressExercises,
        callback: rememberSelfProgressExercise
    });
    initTextExercises();
    initChoiceExercises();
    initSelfProgressExercises();
}
function initTextExercises() {
    (0, _queries.queryTextExercises)().forEach((el)=>{
        const prevAnswer = (0, _clientDb.getValue)(el);
        if (prevAnswer !== null) {
            (0, _queries.queryTextInputs)(el).value = prevAnswer;
            (0, _queries.querySubmitBtn)(el).click();
        }
    });
}
function matchTextExercises(el) {
    return el.classList.contains("short") || el.classList.contains("medium") || el.classList.contains("long");
}
function rememberTextExercise(el) {
    const textElement = (0, _queries.queryTextInputs)(el);
    (0, _telemetry.saveAndSendData)(element, textElement.value);
}
function initChoiceExercises() {
    (0, _queries.queryChoiceExercises)().forEach((el)=>{
        const prevAnswer = (0, _clientDb.getValue)(el);
        if (prevAnswer !== null) {
            const option = (0, _queries.queryOption)(el, prevAnswer);
            const alternative = (0, _queries.queryParentAlternative)(option);
            option.setAttribute("checked", true);
            alternative.classList.add("selected");
            const submitBtn = (0, _queries.querySubmitBtn)(el);
            submitBtn.disabled = false;
            submitBtn.click();
        }
    });
}
function matchChoiceExercises(el) {
    return el.classList.contains("choice");
}
function rememberChoiceExercise(el) {
    const choices = (0, _queries.queryOptions)(el);
    const correctIdx = (0, _queries.queryCorrectOptionIdx)(el);
    for (let choice of choices){
        const alternative = (0, _queries.queryParentAlternative)(choice);
        if (correctIdx === choice.value) alternative.classList.add("correct");
        else alternative.classList.add("wrong");
        if (choice.checked) (0, _telemetry.saveAndSendData)(el, choice.value);
    }
}
function initSelfProgressExercises() {
    (0, _queries.querySelfProgressExercises)().forEach((el)=>{
        const prevAnswer = (0, _clientDb.getValue)(el);
        if (prevAnswer !== null) (0, _queries.querySubmitBtn)(el).click();
    });
}
function matchSelfProgressExercises(el) {
    return el.classList.contains("exercise");
}
function rememberSelfProgressExercise(el) {
    (0, _telemetry.saveAndSendData)(el, true);
}

},{"../client-db":"j0pff","../telemetry":"kpvgZ","./queries":"5VMWX","@parcel/transformer-js/src/esmodule-helpers.js":"5oERU"}],"5VMWX":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "queryTextExercises", ()=>queryTextExercises);
parcelHelpers.export(exports, "queryChoiceExercises", ()=>queryChoiceExercises);
parcelHelpers.export(exports, "querySelfProgressExercises", ()=>querySelfProgressExercises);
parcelHelpers.export(exports, "queryTextInputs", ()=>queryTextInputs);
parcelHelpers.export(exports, "queryOptions", ()=>queryOptions);
parcelHelpers.export(exports, "queryCorrectOptionIdx", ()=>queryCorrectOptionIdx);
parcelHelpers.export(exports, "queryOption", ()=>queryOption);
parcelHelpers.export(exports, "queryParentAlternative", ()=>queryParentAlternative);
parcelHelpers.export(exports, "querySubmitBtn", ()=>querySubmitBtn);
function queryTextExercises() {
    return document.querySelectorAll("div.admonition.exercise.short, div.admonition.exercise.medium, div.admonition.exercise.long");
}
function queryChoiceExercises() {
    return document.querySelectorAll("div.admonition.exercise.choice");
}
function querySelfProgressExercises() {
    return document.querySelectorAll("div.admonition.exercise.self-progress");
}
function queryTextInputs(el) {
    return el.querySelector("input[name='data'], textarea[name='data']");
}
function queryOptions(el) {
    return el.querySelectorAll("input[name='data'][type='radio']");
}
function queryCorrectOptionIdx(el) {
    const alternativeSet = el.querySelector(".alternative-set");
    if (!alternativeSet) return "";
    return alternativeSet.getAttribute("data-answer-idx");
}
function queryOption(el, value) {
    return el.querySelector(`input[name='data'][value='${value}']`);
}
function queryParentAlternative(option) {
    return option.closest(".alternative");
}
function querySubmitBtn(el) {
    return el.querySelector("input[type='submit']");
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"5oERU"}],"70ehP":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
/*
The footnote is structured as follows:
<span class="footnote-container">
  <a class="footnote-anchor">Referenced text goes here</a>
  <div class="footnote-card">
    <li class="footnote-content">Footnote text goes here</li
  </div>
</span>
*/ parcelHelpers.export(exports, "initFooterPlugin", ()=>initFooterPlugin);
var _breakpoints = require("../breakpoints");
function initFooterPlugin(rememberCallbacks) {
    rememberCallbacks.push({
        match: (el)=>el.classList.contains("progress"),
        callback: (el)=>{
            const className = "progress-section";
            const openedSection = el.closest(`.${className}`).nextElementSibling;
            if (!openedSection.classList.contains(className)) return;
            initFootnotes(openedSection);
        }
    });
    initFootnotes(document);
}
function initFootnotes(container) {
    const contentRect = document.getElementsByClassName("ah-content")[0].getBoundingClientRect();
    const footnoteLinks = container.querySelectorAll(".progress-section.show .footnote-ref");
    for (let footnoteLink of footnoteLinks)initFootnote(footnoteLink, contentRect);
}
function initFootnote(footnoteLink, contentRect) {
    const footnoteRef = findRef(footnoteLink);
    const note = findNote(footnoteLink);
    const footnoteCard = setupCard(note);
    const footnoteCloseBtn = setupCloseBtn(footnoteCard);
    const footnoteContainer = setupContainer(footnoteRef, footnoteCard);
    setupCallbacks(footnoteContainer, footnoteRef, footnoteCloseBtn);
    setCustomProps(footnoteContainer, footnoteCard, contentRect);
}
function setupCard(note) {
    const footnoteCard = document.createElement("div");
    footnoteCard.classList.add("footnote-card");
    note.classList.add("footnote-content");
    footnoteCard.appendChild(note);
    return footnoteCard;
}
function setupContainer(footnoteRef, footnoteCard) {
    const footnoteContainer = document.createElement("span");
    footnoteContainer.classList.add("footnote-container");
    if (window.innerWidth > (0, _breakpoints.getBreakpoint)("large", 1440)) footnoteContainer.classList.add("opened");
    // Move to container
    footnoteRef.parentElement.replaceChild(footnoteContainer, footnoteRef);
    footnoteContainer.appendChild(footnoteRef);
    footnoteContainer.appendChild(footnoteCard);
    return footnoteContainer;
}
function setupCloseBtn(footnoteCard) {
    const footnoteCloseBtn = document.createElement("button");
    footnoteCloseBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><!--! Font Awesome Pro 6.2.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M310.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L160 210.7 54.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L114.7 256 9.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L160 301.3 265.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L205.3 256 310.6 150.6z"/></svg>`;
    footnoteCloseBtn.classList.add("footnote-close-btn", "ah-button", "ah-button--borderless");
    footnoteCard.insertBefore(footnoteCloseBtn, footnoteCard.firstChild);
    return footnoteCloseBtn;
}
function setupCallbacks(footnoteContainer, footnoteRef, footnoteCloseBtn) {
    const openedClass = "opened";
    footnoteRef.classList.add("footnote-anchor");
    footnoteRef.addEventListener("click", (event)=>{
        event.preventDefault();
        footnoteContainer.classList.toggle(openedClass);
    });
    footnoteCloseBtn.addEventListener("click", ()=>{
        footnoteContainer.classList.remove(openedClass);
    });
}
function findRef(footnoteLink) {
    return footnoteLink.closest("sup").previousElementSibling;
}
function findNote(footnoteLink) {
    const noteId = footnoteLink.getAttribute("href").substring(1);
    return document.getElementById(noteId);
}
function setCustomProps(footnoteContainer, footnoteCard, contentRect) {
    const offsetX = footnoteContainer.getBoundingClientRect().left;
    const distX = contentRect.right - offsetX;
    footnoteCard.style.setProperty("--dist-x", `${distX}px`);
    footnoteCard.style.setProperty("--offset-x", `${offsetX - contentRect.left}px`);
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"5oERU","../breakpoints":"bXeyp"}],"bXeyp":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "getBreakpoint", ()=>getBreakpoint);
function getBreakpoint(name, defaultVal) {
    return parseInt(window.getComputedStyle(document.documentElement).getPropertyValue(`--breakpoint-${name}`, defaultVal));
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"5oERU"}],"5D3Be":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "initMenuPlugin", ()=>initMenuPlugin);
var _clientDb = require("../client-db");
var _breakpoints = require("../breakpoints");
const btnClass = "ah-menu-btn";
const navClass = "ah-navigation";
const menuOpenedKey = "menu-opened";
function initMenuPlugin() {
    const nav = document.getElementsByClassName(navClass)[0];
    const navContainer = nav.getElementsByClassName("ah-nav-container")[0];
    const menuBtns = document.getElementsByClassName(btnClass);
    if (prefersOpenMenu() && !menuIsOverContent()) openMenu();
    for (let menuBtn of menuBtns)menuBtn.addEventListener("click", function(event) {
        event.stopPropagation();
        toggleMenu(menuBtn);
    });
    const togglableItems = document.getElementsByClassName("ah-togglable-item");
    for (let item of togglableItems){
        const handle = item.getElementsByClassName("ah-togglable-handle")[0];
        handle.addEventListener("click", function(event) {
            event.stopPropagation();
            item.classList.toggle("opened");
        });
    }
    const tocItems = document.getElementsByClassName("ah-toc-item");
    for (let item1 of tocItems)item1.addEventListener("click", function() {
        if (menuIsOverContent()) closeMenu();
    });
    document.addEventListener("click", function(event) {
        if (!nav.classList.contains("show") || !menuIsOverContent()) return;
        if (!navContainer.contains(event.target)) closeMenu();
    });
}
function isMenuOpened() {
    return getNav().classList.contains("show");
}
function menuIsOverContent() {
    return window.innerWidth <= (0, _breakpoints.getBreakpoint)("medium");
}
function getNav() {
    return document.getElementsByClassName(navClass)[0];
}
function openMenu() {
    getNav().classList.add("show");
    (0, _clientDb.setValue)(menuOpenedKey, true);
}
function closeMenu() {
    getNav().classList.remove("show");
    (0, _clientDb.setValue)(menuOpenedKey, false);
}
function prefersOpenMenu() {
    const openedPref = (0, _clientDb.getValue)(menuOpenedKey);
    return openedPref && openedPref == "true";
}
function toggleMenu(menuBtn) {
    if (isMenuOpened(menuBtn)) closeMenu();
    else openMenu();
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"5oERU","../client-db":"j0pff","../breakpoints":"bXeyp"}],"5DGm5":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "initStyle", ()=>initStyle);
function initStyle() {
    const header = document.getElementsByClassName("ah-header")[0];
    document.documentElement.style.setProperty("--header-height", `${header.offsetHeight}px`);
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"5oERU"}]},["1csOT"], null, "parcelRequirea86e")

//# sourceMappingURL=active-handout.a4a697aa.js.map
