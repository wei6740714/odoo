odoo.define('yd_custom_print.custom_print_tag', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');

    var CustomPrintTag = AbstractAction.extend({
        template: 'EmptyComponent',

        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.param = arguments[1]
            if (this.param.context.active_model === undefined) {
                window.history.back()
            }
        },

        willStart: function () {
            if (this.param.context.active_model === undefined) {
                return $.when(
                    this._super.apply(this, arguments),
                    function(){}
                );
            }
            var self = this;


            var fct = this._rpc({
                model: 'yd_custom_print.custom_print',
                method: 'api_init_get_data',
                args: [this.param.context],
            }).then(function (result) {

                self._init_model_data = result;
            });

            //设置
            return $.when(
                this._super.apply(this, arguments),
                fct
            );
        },

        start: function () {
            if (this.param.context.active_model === undefined) {
                return;
            }
            var self = this
            document.documentElement.style.overflowY = "hidden"
            var session_id = window.odoo.session_info.session_id || null;
            var url_param = $.param({
                'session_id': session_id,
                'action_type': self._init_model_data['action_type'],
                'print_model': self._init_model_data['print_model'],
                'related_field': self._init_model_data['related_field'],
                'custom_model_name': self._init_model_data['custom_model_name'],
                'print_model_id': self._init_model_data['print_model_id'] || -1,
                'custom_model_id': self._init_model_data['custom_model_id'] || -1,
            })
            var page
            if (self._init_model_data['action_type'] === 'print') {
                page = 'print.html'
            } else {
                page = 'setting.html'
            }

            var url = "/yd_custom_print/static/hiprint/" + page + '?#' + url_param;
            var css = {width: '100%', height: '250vh'};
            this.$ifr = $('<iframe/>').attr('src', url);
            this.$ifr.attr('frameborder', '0');
            this.$ifr.appendTo(this.$el).css(css);
            return this._super();
        },
    });
    core.action_registry.add('yd_custom_print.action_custom_print_tag', CustomPrintTag);
    return CustomPrintTag;
});
