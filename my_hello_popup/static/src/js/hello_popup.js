/** @odoo-module **/

odoo.define('my_hello_popup.hello_popup', function (require) {
    "use strict";
    document.addEventListener("DOMContentLoaded", function () {
        console.log("✅ hello_popup.js carregado com sucesso.");
        alert("Hello!");
    });
});
