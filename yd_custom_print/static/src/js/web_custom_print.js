odoo.define('yd_custom_print', function (require) {
    "use strict";

    var core = require('web.core');
    var Sidebar = require('web.Sidebar');
    var session = require('web.session');
    var crash_manager = require('web.crash_manager');

    var QWeb = core.qweb;
    var ajax = require('web.ajax');
    var ActionManager = require("web.ActionManager");
    var _t = core._t;
    // var testUtils = require('web.test_utils');
    // var createActionManager = testUtils.createActionManager;

    Sidebar.include({

        _redraw: function () {
            var self = this;
            var searchParams = new URLSearchParams(window.location.href.split('#')[1]);
            var model_name = searchParams.get('model');
            this._super.apply(this, arguments);
            if (self.getParent().renderer.viewType === 'form') {
                this._rpc({
                    model: 'yd_custom_print.custom_print',
                    method: 'api_model_print_list',
                    args: [model_name],
                }).then(function (result) {
                    if (!result.length){
                        return
                    }
                    let custom_print_btn = self.$el.find('#show-print-item');
                    if (!custom_print_btn.length) {

                        let printbtn = QWeb.render(
                            'WebCustomPrintBtn', {widget: self})
                        self.$el.find('.o_dropdown')
                            .parent().append(printbtn);

                        let $ul_list = self.$el.find('#show-print-item');
                        let print_items = QWeb.render(
                            'WebCustomPrintItem', {widget: self, columns: result})
                        $ul_list.append(print_items)

                        let li_list = $ul_list.find('li')

                        _.each(li_list, function (val) {
                            let $val = $(val)
                            $val.on('click',null,$val.text().trim(),self.on_jump_print_page)
                        })

                    }
                });
            }
        },


        on_jump_print_page: function (ev) {
           ev.preventDefault();
            ev.stopPropagation();
            let custom_model_name=ev.data
            var self = this;
            var searchParams = new URLSearchParams(window.location.href.split('#')[1]);
            searchParams.set('view_type', 'form');
            var res_id = searchParams.get('id')
            var model = searchParams.get('model');

            var action = {
                type: 'ir.actions.client',
                tag: 'yd_custom_print.action_custom_print_tag',
                context: {
                    active_id: res_id,
                    active_model: model,
                    action_type: 'print',
                    custom_model_name:custom_model_name,
                },
            };

            self.do_action(action)

        },

    });
});
