# Copyright 2016 Henry Zhou (http://www.maxodoo.com)
# Copyright 2016 Rodney (http://clearcorp.cr/)
# Copyright 2012 Agile Business Group
# Copyright 2012 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json
import odoo.http as http
from odoo.http import request
from odoo.addons.web.controllers.main import ExcelExport


class yd_custom_print(http.Controller):
    #保存或修改数据


    #读取数据
    @http.route('/api/v1/yd_custom_print/previous_data/', auth='public', type='json', methods=['Get', 'POST'])
    def previous_data(self, model, res_id, fields):
        print('test')
        request.env.ref('yd_custom_print.action_custom_print').id
        request.env['yd_custom_print.custom_print'].browse(1)
        production = request.env[model].browse(int(res_id))
        return {}

    @http.route('/api/v1/yd_custom_print/get_action_tag_id/', auth='public', type='json', methods=['Get', 'POST'])
    def previous_data(self, *args,**kwargs):
        action_id=request.env.ref('yd_custom_print.action_custom_print').id
        tag_name='yd_custom_print.action_custom_print'
        print('test')
        return {
            'tag_name':tag_name,
            'action_id':action_id,
        }

    #基础模板




    # @http.route('/web/export/xls_view', type='http', auth='user')
    # def export_xls_view(self, data, token):
    #     data = json.loads(data)
    #     model = data.get('model', [])
    #     columns_headers = data.get('headers', [])
    #     rows = data.get('rows', [])
    #
    #     return request.make_response(
    #         self.from_data(columns_headers, rows),
    #         headers=[
    #             ('Content-Disposition', 'attachment; filename="%s"'
    #              % self.filename(model)),
    #             ('Content-Type', self.content_type)
    #         ],
    #         cookies={'fileToken': token}
    #     )
