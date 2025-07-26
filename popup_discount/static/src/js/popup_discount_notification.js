odoo.define('popup_discount.notification', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    function show_notification(message, type) {
        var $notification = $('<div class="o_notification"/>')
            .addClass('alert-' + type)
            .text(message)
            .appendTo('body');
        
        setTimeout(function() {
            $notification.fadeOut(500, function() {
                $(this).remove();
            });
        }, 5000);
    }

    return {
        show_notification: show_notification
    };
});
