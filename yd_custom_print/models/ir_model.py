from odoo import fields, models, api
from odoo import _

class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'


    # @api.multi
    # def name_get(self):
    #     res = []
    #     for field in self:
    #         res.append((field.id, '%s (%s)' % (_(field.field_description), field.model)))
    #     return res


        # if self._context.get('only_show_name'):
        #     res = []
        #     for field in self:
        #         res.append((field.id, '%s (%s)' % (_(field.field_description), field.name)))
        #     return res
        # else:
        #     return super().name_get()


    # def _compute_complete_name(self):
    #     for res in self:
    #         res.complete_name = ".".join(n for n in [_(res.field_description), res.model] if n)