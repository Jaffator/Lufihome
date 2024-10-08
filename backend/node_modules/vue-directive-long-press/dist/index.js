"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var longPressStop = new CustomEvent('long-press-stop');
var longPressStart = new CustomEvent('long-press-start');
exports.directiveOption = {
    bind: function (el, binding, vnode) {
        el.dataset.longPressTimeoutId = '0';
        var onpointerup = function () {
            clearTimeout(parseInt(el.dataset.longPressTimeoutId));
            if (vnode.componentInstance) {
                vnode.componentInstance.$emit('long-press-stop');
            }
            else {
                el.dispatchEvent(longPressStop);
            }
            document.removeEventListener('pointerup', onpointerup);
        };
        var onpointerdown = function () {
            document.addEventListener('pointerup', onpointerup);
            var timeout = setTimeout(function () {
                if (vnode.componentInstance) {
                    vnode.componentInstance.$emit('long-press-start');
                }
                else {
                    el.dispatchEvent(longPressStart);
                }
            }, binding.value);
            el.dataset.longPressTimeoutId = timeout.toString();
        };
        el.$_long_press_pointerdown_handler = onpointerdown;
        el.addEventListener('pointerdown', onpointerdown);
    },
    unbind: function (el) {
        clearTimeout(parseInt(el.dataset.longPressTimeoutId));
        el.removeEventListener('pointerdown', el.$_long_press_pointerdown_handler);
    }
};
exports.default = exports.directiveOption;
//# sourceMappingURL=index.js.map