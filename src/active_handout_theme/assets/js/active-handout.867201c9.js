!function(){function e(e,t,n,r){Object.defineProperty(e,t,{get:n,set:r,enumerable:!0,configurable:!0})}var t=("undefined"!=typeof globalThis?globalThis:"undefined"!=typeof self?self:"undefined"!=typeof window?window:"undefined"!=typeof global?global:{}).parcelRequirea86e;t.register("62Rfj",(function(e,n){var r=t("9GMMU"),o=t("7zxXP"),s=t("iN7fV"),i=t("jc3XN"),c=t("kUxQr"),u=t("7srJm"),a=t("iGX1C");function l(){(0,r.initTabbedPlugin)();let e=[];window.addEventListener("remember",(function(t){const n=t.detail.element;for(let r of e)if(r.match(n)){if(r.callback(n,t.detail.args))break}})),(0,a.initStyle)(),(0,s.initMenuPlugin)(),(0,o.initProgressPlugin)(e),(0,u.initParsonsPlugin)(e),(0,i.initExercisePlugin)(e),(0,c.initFooterPlugin)(e)}"loading"!==document.readyState?l():document.addEventListener("DOMContentLoaded",l)})),t.register("9GMMU",(function(t,n){e(t.exports,"initTabbedPlugin",(function(){return r}));function r(){(()=>{const e=e=>{const t=e.target;if(!e.target.matches(".tabbed-labels"))return;const n=t.scrollWidth-t.clientWidth;if(t.classList.remove("tabbed-scroll","tabbed-scroll-left","tabbed-scroll-right"),"resize"===e.type||"scroll"===e.type){if(0===n)return;t.classList.add("tabbed-scroll"),t.scrollLeft?t.scrollLeft<n-3?t.classList.add("tabbed-scroll-left","tabbed-scroll-right"):t.classList.add("tabbed-scroll-left"):t.classList.add("tabbed-scroll-right")}},t=e=>{const t=e.target,n=t.closest(".tabbed-set").querySelector("input:checked");let r=null;if(t.classList.contains("tabbed-scroll-right")&&e.offsetX>=e.target.offsetWidth-15){const e=n.nextSibling;r=n,e&&"INPUT"===e.tagName&&(r=e)}else if(t.classList.contains("tabbed-scroll-left")&&e.offsetX<=15){const e=n.previousSibling;r=n,e&&"INPUT"===e.tagName&&(r=e)}r&&r.click()},n=new ResizeObserver((t=>{t.forEach((t=>{e({target:t.target,type:"resize"})}))}));document.querySelectorAll(".tabbed-alternate > .tabbed-labels").forEach((r=>{e({target:r,type:"resize"}),n.observe(r),r.addEventListener("resize",e),r.addEventListener("scroll",e),r.addEventListener("click",t)}))})(),(()=>{const e=document.querySelectorAll(".tabbed-alternate > input");for(const t of e)t.addEventListener("change",(()=>{document.querySelector(`label[for=${t.id}]`).scrollIntoView({block:"nearest",inline:"nearest",behavior:"smooth"})}))})()}})),t.register("7zxXP",(function(n,r){e(n.exports,"initProgressPlugin",(function(){return i}));var o=t("lw4dE"),s=t("fHWZd");function i(e){e.push({match:e=>e.classList.contains("progress"),callback:e=>{(0,s.saveAndSendData)(e,!0)}}),document.querySelectorAll("button.progress").forEach((e=>{(0,o.getValue)(e)&&e.click()}))}})),t.register("lw4dE",(function(t,n){function r(e){if("string"==typeof e)return e;const t=document.location.pathname,n=t.endsWith("/")?"":"/";return`${t}${n}${e.id}`}function o(e,t){const n=r(e);localStorage[n]=t}function s(e){const t=r(e);return localStorage.getItem(t)}function i(e){const t=r(e);localStorage.removeItem(t)}e(t.exports,"setValue",(function(){return o})),e(t.exports,"getValue",(function(){return s})),e(t.exports,"removeValue",(function(){return i}))})),t.register("fHWZd",(function(n,r){e(n.exports,"saveAndSendData",(function(){return s}));var o=t("lw4dE");function s(e,t){(0,o.setValue)(e,t)}})),t.register("iN7fV",(function(n,r){e(n.exports,"initMenuPlugin",(function(){return u}));var o=t("lw4dE"),s=t("iy2zE");const i="ah-navigation",c="menu-opened";function u(){const e=document.getElementsByClassName(i)[0],t=e.getElementsByClassName("ah-nav-container")[0],n=document.getElementsByClassName("ah-menu-btn"),r=document.getElementsByClassName("close-menu")[0];(function(){const e=(0,o.getValue)(c);return e&&"true"==e})()&&!a()&&d();for(let e of n)e.addEventListener("click",(function(t){t.stopPropagation(),m(e)}));const s=document.getElementsByClassName("ah-togglable-item");for(let e of s){e.getElementsByClassName("ah-togglable-handle")[0].addEventListener("click",(function(t){t.stopPropagation(),e.classList.toggle("opened")}))}const u=document.getElementsByClassName("ah-toc-item");for(let e of u)e.addEventListener("click",(function(){a()&&f()}));r.addEventListener("click",f),document.addEventListener("click",(function(n){e.classList.contains("show")&&a()&&(t.contains(n.target)||f())}))}function a(){return window.innerWidth<=(0,s.getBreakpoint)("large")}function l(){return document.getElementsByClassName(i)[0]}function d(){l().classList.add("show"),(0,o.setValue)(c,!0)}function f(){l().classList.remove("show"),(0,o.setValue)(c,!1)}function m(e){l().classList.contains("show")?f():d()}})),t.register("iy2zE",(function(t,n){function r(e,t){return parseInt(window.getComputedStyle(document.documentElement).getPropertyValue(`--breakpoint-${e}`,t))}e(t.exports,"getBreakpoint",(function(){return r}))})),t.register("jc3XN",(function(n,r){e(n.exports,"initExercisePlugin",(function(){return c}));var o=t("lw4dE"),s=t("fHWZd"),i=t("hxUu7");function c(e){e.push({match:u,callback:a},{match:l,callback:d},{match:f,callback:m}),(0,i.queryTextExercises)().forEach((e=>{const t=(0,o.getValue)(e);if(null!==t){const n=(0,i.queryTextInputs)(e);n.value=t;const r=n.closest(".grow-wrap");r&&(r.dataset.replicatedValue=t),(0,i.querySubmitBtn)(e).click()}})),(0,i.queryChoiceExercises)().forEach((e=>{const t=(0,o.getValue)(e);if(null!==t){const n=(0,i.queryOption)(e,t),r=(0,i.queryParentAlternative)(n);n.setAttribute("checked",!0),r.classList.add("selected");const o=(0,i.querySubmitBtn)(e);o.disabled=!1,o.click()}})),(0,i.querySelfProgressExercises)().forEach((e=>{null!==(0,o.getValue)(e)&&(0,i.querySubmitBtn)(e).click()})),document.getElementById("resetHandoutButton").addEventListener("click",(function(){const e=document.querySelectorAll(".admonition.exercise");for(const t of e)(0,o.removeValue)(t);location.reload()}))}function u(e){return e.classList.contains("short")||e.classList.contains("medium")||e.classList.contains("long")}function a(e){const t=(0,i.queryTextInputs)(e);return(0,s.saveAndSendData)(e,t.value),!0}function l(e){return e.classList.contains("choice")}function d(e){const t=(0,i.queryOptions)(e),n=(0,i.queryCorrectOptionIdx)(e);for(let r of t){const t=(0,i.queryParentAlternative)(r);n===r.value?t.classList.add("correct"):t.classList.add("wrong"),r.checked&&(0,s.saveAndSendData)(e,r.value)}return!0}function f(e){return e.classList.contains("self-progress")}function m(e){return(0,s.saveAndSendData)(e,!0),!0}})),t.register("hxUu7",(function(t,n){function r(){return document.querySelectorAll("div.admonition.exercise.short, div.admonition.exercise.medium, div.admonition.exercise.long")}function o(){return document.querySelectorAll("div.admonition.exercise.choice")}function s(){return document.querySelectorAll("div.admonition.exercise.self-progress")}function i(e){return e.querySelector("input[name='data'], textarea[name='data']")}function c(e){return e.querySelectorAll("input[name='data'][type='radio']")}function u(e){const t=e.querySelector(".alternative-set");return t?t.getAttribute("data-answer-idx"):""}function a(e,t){return e.querySelector(`input[name='data'][value='${t}']`)}function l(e){return e.closest(".alternative")}function d(e){return e.querySelector("input[type='submit']")}e(t.exports,"queryTextExercises",(function(){return r})),e(t.exports,"queryChoiceExercises",(function(){return o})),e(t.exports,"querySelfProgressExercises",(function(){return s})),e(t.exports,"queryTextInputs",(function(){return i})),e(t.exports,"queryOptions",(function(){return c})),e(t.exports,"queryCorrectOptionIdx",(function(){return u})),e(t.exports,"queryOption",(function(){return a})),e(t.exports,"queryParentAlternative",(function(){return l})),e(t.exports,"querySubmitBtn",(function(){return d}))})),t.register("kUxQr",(function(n,r){e(n.exports,"initFooterPlugin",(function(){return s}));var o=t("iy2zE");function s(e){e.push({match:e=>e.classList.contains("progress"),callback:e=>{const t="progress-section",n=e.closest(`.${t}`).nextElementSibling;n.classList.contains(t)&&i(n)}}),i(document)}function i(e){const t=document.getElementsByClassName("ah-content")[0].getBoundingClientRect(),n=e.querySelectorAll(".progress-section.show .footnote-ref");for(let e of n)c(e,t)}function c(e,t){const n=function(e){return e.closest("sup").previousElementSibling}(e),r=function(e){const t=e.getAttribute("href").substring(1);return document.getElementById(t)}(e),s=function(e){const t=document.createElement("div");return t.classList.add("footnote-card"),e.classList.add("footnote-content"),t.appendChild(e),t}(r),i=function(e){const t=document.createElement("button");return t.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">\x3c!--! Font Awesome Pro 6.2.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --\x3e<path d="M310.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L160 210.7 54.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L114.7 256 9.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L160 301.3 265.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L205.3 256 310.6 150.6z"/></svg>',t.classList.add("footnote-close-btn","ah-button","ah-button--borderless"),e.insertBefore(t,e.firstChild),t}(s),c=function(e,t){const n=document.createElement("span");n.classList.add("footnote-container"),window.innerWidth>(0,o.getBreakpoint)("large",1440)&&n.classList.add("opened");return e.parentElement.replaceChild(n,e),n.appendChild(e),n.appendChild(t),n}(n,s);!function(e,t,n){const r="opened";t.classList.add("footnote-anchor"),t.addEventListener("click",(t=>{t.preventDefault(),e.classList.toggle(r)})),n.addEventListener("click",(()=>{e.classList.remove(r)}))}(c,n,i),function(e,t,n){const r=e.getBoundingClientRect().left,o=n.right-r;t.style.setProperty("--dist-x",`${o}px`),t.style.setProperty("--offset-x",r-n.left+"px")}(c,s,t)}})),t.register("7srJm",(function(n,r){e(n.exports,"initParsonsPlugin",(function(){return c}));var o=t("2tIiG"),s=t("9whkM"),i=t("fHWZd");function c(e){(0,o.queryParsonsExercises)().forEach(u),e.push({match:e=>e.classList.contains("parsons"),callback:(e,{correct:t})=>((0,i.saveAndSendData)(e,t),!0)})}function u(e){const t=(0,o.queryDropArea)(e),n=(0,o.queryDragArea)(e);let r=null;function i(t){t.preventDefault(),(0,s.eventIsInsideExercise)(t,e)&&(0,s.setCurrentSubslot)((0,o.selectSubslotUnderCursor)(t,e),e)}function c(t){t.preventDefault(),(0,s.removeDragListeners)(i,c),(0,s.eventIsInsideExercise)(t,e)&&(0,s.insertLineInSubslot)(r,(0,o.selectSubslotUnderCursor)(t,e)),(0,s.cleanUpSlots)(e),r=null}function u(e){(0,s.addDragListeners)(i,c),(0,s.createSlot)(n,1,"single-subslot"),(0,s.createSlot)(t,6),r=e.target,(0,s.hide)(r)}(0,o.queryResetButton)(e).addEventListener("click",(()=>(0,s.resetExercise)(e))),(0,o.querySubmitButton)(e).addEventListener("click",(()=>(0,s.submitExercise)(e))),(0,o.queryParsonsLines)(e).forEach((e=>{e.addEventListener("dragstart",u)}))}})),t.register("2tIiG",(function(t,n){function r(){return document.querySelectorAll("div.admonition.exercise.parsons")}function o(e){return e.querySelector("input[name=resetButton]")}function s(e){return e.querySelector("input[name=sendButton]")}function i(e){return e.querySelector(".admonition.answer")}function c(e){return e.querySelectorAll(".parsons-container")}function u(e){return e.querySelector(".parsons-drop-area")}function a(e){return e.querySelector(".parsons-drag-area")}function l(e){return e.querySelectorAll(".parsons-line")}function d(e){return e.querySelector(".line-slot:last-child")}function f(e){return e.querySelectorAll(".line-slot")}function m(e){return e.querySelectorAll(".subslot")}function p(e){return e.querySelector(".line-slot:not(.with-line)")}function g(e){return e.closest(".line-slot")}function y(e){return e.closest(".parsons-area")}function h(e){return e.closest(".parsons-container")}function v(e,t){const n=x(e,"subslot");if(n)return n;const r=function(e,t){const n=x(e,"line-slot");if(n)return n;const r=x(e,"parsons-container");return r?p(r):function(e){return e.querySelector(".line-slot.drag-over")}(t)}(e,t);return r.querySelector(".subslot")}function b(e){return x(e,"exercise")}function x(e,t){const n=document.elementsFromPoint(e.clientX,e.clientY);for(let e=0;e<n.length;e++)if(n[e].classList.contains(t))return n[e]}e(t.exports,"queryParsonsExercises",(function(){return r})),e(t.exports,"queryResetButton",(function(){return o})),e(t.exports,"querySubmitButton",(function(){return s})),e(t.exports,"queryAnswer",(function(){return i})),e(t.exports,"queryParsonsContainers",(function(){return c})),e(t.exports,"queryDropArea",(function(){return u})),e(t.exports,"queryDragArea",(function(){return a})),e(t.exports,"queryParsonsLines",(function(){return l})),e(t.exports,"queryLastSlot",(function(){return d})),e(t.exports,"querySlots",(function(){return f})),e(t.exports,"querySubslots",(function(){return m})),e(t.exports,"queryEmptySlot",(function(){return p})),e(t.exports,"querySlotFromInside",(function(){return g})),e(t.exports,"queryAreaFromInside",(function(){return y})),e(t.exports,"queryContainerFromInside",(function(){return h})),e(t.exports,"selectSubslotUnderCursor",(function(){return v})),e(t.exports,"selectExerciseUnderCursor",(function(){return b}))})),t.register("9whkM",(function(n,r){e(n.exports,"removeDragListeners",(function(){return i})),e(n.exports,"addDragListeners",(function(){return c})),e(n.exports,"insertLineInSubslot",(function(){return u})),e(n.exports,"eventIsInsideExercise",(function(){return a})),e(n.exports,"setCurrentSubslot",(function(){return l})),e(n.exports,"createSlot",(function(){return d})),e(n.exports,"hide",(function(){return f})),e(n.exports,"cleanUpSlots",(function(){return m})),e(n.exports,"resetExercise",(function(){return p})),e(n.exports,"submitExercise",(function(){return g}));var o=t("6fdZM"),s=t("2tIiG");function i(e,t){window.removeEventListener("dragenter",e),window.removeEventListener("dragover",e),window.removeEventListener("drop",t)}function c(e,t){window.addEventListener("dragenter",e),window.addEventListener("dragover",e),window.addEventListener("drop",t)}function u(e,t){if(!t)return;const n=(0,s.querySlotFromInside)(t);n.classList.remove("drag-over"),n.classList.add("with-line"),t.classList.remove("drag-over"),t.classList.add("cur-indent"),n.appendChild(e)}function a(e,t){return(0,s.selectExerciseUnderCursor)(e)===t}function l(e,t){if(!e)return;const n=(0,s.querySlotFromInside)(e);n.classList.add("drag-over"),e.classList.add("drag-over"),(0,s.querySlots)(t).forEach((e=>{e!==n&&e.classList.remove("drag-over")})),(0,s.querySubslots)(t).forEach((t=>{t!==e&&t.classList.remove("drag-over")})),y(n);const r=(0,s.queryContainerFromInside)(n);!function(e,t){e.forEach((e=>{e!==t&&y((0,s.queryLastSlot)(e))}))}((0,s.queryParsonsContainers)(t),r),r.classList.add("drag-over")}function d(e,t,n){const r=(0,o.createElementWithClasses)("div",["line-slot"],e),s=["subslot"];n&&s.push(n);for(let e=0;e<t;e++)(0,o.createElementWithClasses)("div",[...s,`subslot-${e+1}`],r);(0,o.createElementWithClasses)("div",["line-placeholder"],r)}function f(e){setTimeout((()=>{(0,s.querySlotFromInside)(e).classList.add("dragging")}),0)}function m(e){const t=(0,s.querySlots)(e);for(let e of t)e.classList.remove("dragging"),0===(0,s.queryParsonsLines)(e).length&&e.remove()}function p(e){(0,s.queryAnswer)(e).style.display="none";const t=(0,s.queryDragArea)(e),n=(0,s.queryDropArea)(e);(0,s.queryParsonsLines)(n).forEach((e=>{const n=(0,s.querySlotFromInside)(e),r=(0,o.createElementWithClasses)("div",["line-slot","with-line"],t);(0,o.createElementWithClasses)("div",["subslot","cur-indent","single-subslot"],r),(0,o.createElementWithClasses)("div",["line-placeholder"],r),r.appendChild(e),n.remove()}))}function g(e){e.classList.remove("correct"),e.classList.remove("wrong");const t=(0,s.queryDragArea)(e),n=(0,s.queryDropArea)(e),r=(0,s.queryParsonsLines)(n);let i=r.length>0&&0===(0,s.queryParsonsLines)(t).length,c=e.querySelector('input[name="answer"]');console.log(c.value);let u="";r.forEach(((e,t)=>{const n=(0,s.querySlotFromInside)(e),r=parseInt(e.dataset.lineNum)===t,o=parseInt(e.dataset.indentcount)===h(n);u+="    ".repeat(h(n))+n.innerText+"\n",i&&(i=r&&o)})),console.log(u),setTimeout((()=>{i?e.classList.add("correct"):e.classList.add("wrong")}),0),(0,s.queryAnswer)(e).style.display="inherit",(0,o.sendRemember)(e,{correct:i})}function y(e){if(!e.classList.contains("with-line"))return;const t=(0,s.queryAreaFromInside)(e),n=(0,s.queryEmptySlot)(t);!function(e,t,n){for(let r of(0,s.querySlots)(e)){if(r===t)return!0;if(r===n)return!1}return!1}(t,n,e)?t.insertBefore(n,e):t.insertBefore(n,e.nextSibling)}function h(e){const t=e.querySelector(".subslot.cur-indent"),n="subslot-";for(let e of t.classList)if(e.startsWith(n)){const t=parseInt(e.substr(n.length));if(t)return t-1}return 0}})),t.register("6fdZM",(function(t,n){function r(e,t,n){const r=document.createElement(e);for(let e of t)r.classList.add(e);return n&&n.appendChild(r),r}function o(e,t){const n=new CustomEvent("remember",{detail:{element:e,args:t}});window.dispatchEvent(n)}e(t.exports,"createElementWithClasses",(function(){return r})),e(t.exports,"sendRemember",(function(){return o}))})),t.register("iGX1C",(function(t,n){function r(){const e=document.getElementsByClassName("ah-header")[0];document.documentElement.style.setProperty("--header-height",`${e.offsetHeight}px`),window.addEventListener("resize",(()=>{let e=.01*window.innerHeight;document.documentElement.style.setProperty("--vh",`${e}px`)})),document.querySelectorAll(".grow-wrap").forEach((e=>{const t=e.querySelector("textarea");t.addEventListener("input",(()=>{e.dataset.replicatedValue=t.value}))}))}e(t.exports,"initStyle",(function(){return r}))}))}();
//# sourceMappingURL=active-handout.867201c9.js.map
