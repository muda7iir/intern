/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { Popover } from "@web/core/popover/popover";

/*
 * Fix for Odoo 19 cross-origin iframe SecurityError.
 * The web_mobile module patches Popover.setup() and calls useClickAway()
 * which tries to access window.parent.addEventListener. When Odoo is
 * rendered inside the Odoo.sh editor iframe, this throws a SecurityError
 * because the parent frame is on a different origin.
 *
 * This patch wraps setup() in a try-catch to gracefully handle the error.
 */
patch(Popover.prototype, {
    setup() {
        try {
            super.setup(...arguments);
        } catch (e) {
            if (e instanceof DOMException && e.name === "SecurityError") {
                console.warn(
                    "nx_intern_training: Suppressed cross-origin SecurityError in Popover.setup"
                );
                return;
            }
            throw e;
        }
    },
});
