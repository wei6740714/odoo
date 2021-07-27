# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from lxml import etree
from lxml.builder import E
import pickle
import datetime


from .register_list import g_register_print_list
from .common_field_no_needed import g_common_field_no_needed

def get_model_id_set():
    model_set = set()
    for val in g_register_print_list:
        model_name = val['model_name']
        model_set.add(model_name)
    return list(model_set)
_model_id_names=get_model_id_set()

class custom_print(models.Model):
    _name = 'yd_custom_print.custom_print'

    _sql_constraints = [
        ('name_uniq', 'unique (name)', '名称必须唯一!')
    ]

    name = fields.Char(string='名称')

    model_id = fields.Many2one(
        comodel_name='ir.model',
        string='模型',
        domain=[('model','in',_model_id_names)],
        required=True)

    tree_field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='对应的列表',
        required=True)

    json_data = fields.Binary('字段数据')

    header_field_needed_ids = fields.One2many(
        comodel_name='yd_custom_print.header_field_needed',
        inverse_name='custom_print_id',
        string='需要的头部字段',copy=False,
        required=False)

    tree_field_needed_ids = fields.One2many(
        comodel_name='yd_custom_print.tree_field_needed',
        inverse_name='custom_print_id',
        string='需要的列表字段',copy=False,
        required=False)



    @api.onchange('model_id')
    def onchange_model_id(self):
        # self.tree_field_id=None

        tree_field_id_set = set()
        for val in g_register_print_list:
            if self.model_id.model==val['model_name']:
                tree_field_id_set.add(val['related_tree_filed'])

        tree_field_domain= [('name','in',list(tree_field_id_set)),('model', '=',self.model_id.model)]
        
        self.tree_field_id=self.tree_field_id.search(tree_field_domain,limit=1)
        
        return {'domain': {
            'tree_field_id': tree_field_domain,
        }}

    @api.onchange('tree_field_id')
    def onchange_tree_field_id(self):
        if not self.model_id:
            return

        IrModelFields=self.env['ir.model.fields'].sudo()
        # 头部字段
        self.header_field_needed_ids=[(6,0,[])]
        field_ids = IrModelFields.search([('model', '=', self.model_id.model),
                                          ('name','not in',g_common_field_no_needed),
                                          ('ttype','!=','one2many')
                                          ]).ids
        values = []
        for field_id in field_ids:
            val = {'field_id':field_id,'is_need':True}
            values.append(val)

        self.header_field_needed_ids = values

        # 列表字段
        self.tree_field_needed_ids=[(6,0,[])]
        tree_obj=getattr(self.env[self.model_id.model], self.tree_field_id.name)
        field_ids = IrModelFields.search([('model', '=', tree_obj._name),
                                          ('name','not in',g_common_field_no_needed),
                                          ('ttype', '!=', 'one2many')
                                          ]).ids
        values = []
        for field_id in field_ids:
            val = {'field_id':field_id,'is_need':True}
            values.append(val)

        self.tree_field_needed_ids = values







class custom_print_header_field_filter(models.Model):
    _name = 'yd_custom_print.header_field_needed'

    name = fields.Char(string='名称',compute='_compute_name')


    field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='字段名称',
        required=True)

    custom_print_id = fields.Many2one(
        comodel_name='yd_custom_print.custom_print',
        string='打印模型',
        required=True,
        ondelete = 'cascade',
    )
    is_need = fields.Boolean('是否需要',default=True)

    def _compute_name(self):
        for rec in self:
            rec.name=_(rec.field_id.field_description)


class custom_print_tree_field_filter(models.Model):
    _name = 'yd_custom_print.tree_field_needed'

    name = fields.Char(string='名称',compute='_compute_name')

    field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='字段名称',
        required=True)

    custom_print_id = fields.Many2one(
        comodel_name='yd_custom_print.custom_print',
        string='打印模型',
        required=True,
        ondelete = 'cascade',
    )

    is_need=fields.Boolean('是否需要',default=True)

    def _compute_name(self):
        for rec in self:
            rec.name=_(rec.field_id.field_description)