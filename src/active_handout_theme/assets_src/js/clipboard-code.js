import Clipboard from "clipboard";

export function initClipBoard() {
    // https://clipboardjs.com/
    var selectors = document.querySelectorAll('pre code');
    var copyButton =
    '<div class="clipboard"><span class="btn btn-neutral btn-clipboard" title="Copy to clipboard"> <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 21H8V7h11m0-2H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2m-3-4H4a2 2 0 0 0-2 2v14h2V3h12V1Z"/></svg> </span></div>';

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
