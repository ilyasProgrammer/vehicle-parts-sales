odoo.define('website_links.website_links', function (require) {
    'use strict';
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var base = require('web_editor.base');
    var website = require('website.website');
    var Model = require('web.Model');
    var qweb = core.qweb;
    var _t = core._t;

    base.ready().done(function() {
        $('#add_vin').click(function() {
            ajax.jsonRpc("/web/add_vin", 'call', {'car_name': $("#car_name").val(),
                                                  'car_vin': $("#car_vin").val(),
                                                }).then(function (result) {
                        var link = result[0];
            });
        });
    });

});
