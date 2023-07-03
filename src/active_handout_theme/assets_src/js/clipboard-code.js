import Clipboard from "clipboard";

export function initClipBoard() {
    // https://clipboardjs.com/
    var selectors = document.querySelectorAll('pre code');
    var copyButton = '<div class="clipboard"><span class="btn btn-neutral btn-clipboard" title="Copy to clipboard"> "Copy" </span></div>';
    Array.prototype.forEach.call(selectors, function(selector){
        selector.insertAdjacentHTML('beforebegin', copyButton);
    });

    var clipboard = new Clipboard('.btn-clipboard', {
        target: function (trigger) {
        return trigger.parentNode.nextElementSibling;
        }
    });

    clipboard.on('success', function (e) {
        e.clearSelection();
    });
};
