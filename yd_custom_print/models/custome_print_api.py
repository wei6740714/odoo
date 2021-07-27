# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from lxml import etree
from lxml.builder import E
import pickle,json
import datetime




class custom_print(models.Model):
    _inherit = 'yd_custom_print.custom_print'


    @api.model
    def register_print_model(self,model_name,related_tree_filed):
        '''
        注册模型的名称和相关的字段名,也可直接在文件register_list添加.
        '''
        from .register_list import g_register_print_list
        o={
            'model_name':model_name,
            'related_tree_filed':related_tree_filed,
        }
        if o not in g_register_print_list:
            g_register_print_list.append(o)

    @api.model
    def api_model_print_list(self, model_name=None, ):
        '''
            form表单视图下拉得到列表
        '''
        name_list = self.search([('model_id.model', '=', model_name)]).mapped('name')

        return name_list

    @api.model
    def api_init_get_data(self, context=None, ):
        '''
        得到初始化数据
        '''
        if context.get('active_model') == self._name:
            active_id = int(context.get('active_id'))
            custom_model = self.browse(active_id)

            result = {
                'action_type': 'setting',
                'custom_model_id': custom_model.id,
                'print_model': custom_model.model_id.model,
                'related_field': custom_model.tree_field_id.name,
            }
            return result

        else:
            active_id=int(context.get('active_id'))
            print_model = self.env[context.get('active_model')].browse(active_id)
            custom_model = self.search([('model_id.model', '=', print_model._name),('name','=',context.get('custom_model_name'))])
            result = {
                'action_type': 'print',
                'print_model': custom_model.model_id.model,
                'print_model_id': print_model.id,
                'related_field': custom_model.tree_field_id.name,
                'custom_model_name': custom_model.name,
            }
            return result

    @api.model
    def api_save_json_data(self, odoo_data=None,save_data=None):
        '''
        保存json数据
        '''
        custom_model=self._get_custom_model(odoo_data)
        custom_model.json_data=pickle.dumps(save_data)
        return {'state':'ok'}

    @api.model
    def api_read_json_data(self, odoo_data=None):
        '''
        得到json数据
        '''
        custom_model = self._get_custom_model(odoo_data)
        if not custom_model.json_data:
            # 设置默认数据
            from .default_data import default_data
            custom_model.json_data=pickle.dumps(json.dumps(default_data))
        saved_data=pickle.loads(custom_model.json_data)
        return {'saved_data': saved_data}


    @api.model
    def api_read_print_need_json_data(self, odoo_data=None):
        '''
        打印时需要的字段数据
        '''

        custom_model=self._get_custom_model(odoo_data)
        header_valid_fields = self._filter_header_fileds(custom_model)
        tree_valid_fields=self._filter_tree_fileds(custom_model)

        result=self._get_instance_header_field2value(odoo_data,header_valid_fields)
        result['table']=self._get_instance_tree_field2value(odoo_data,tree_valid_fields)

        return result

    @api.model
    def api_read_print_default_json_data(self, odoo_data=None):
        '''
        读取保存的模板或是默认模板
        '''
        custom_model = self._get_custom_model(odoo_data)
        if not custom_model:
            custom_model.json_data=b""
        saved_data=pickle.loads(custom_model.json_data)
        return {'saved_data': saved_data}


    @api.model
    def api_init_get_field_data(self, odoo_data=None):
        '''
        读取初始的字段,包括表头的字典和列表的字段(字段+字段名称)
        '''
        custom_model_id = int(odoo_data.get('custom_model_id'))
        related_field = odoo_data.get('related_field')
        custom_print = self.browse(custom_model_id)
        result = {}

        header_data = self._get_header_field2string(custom_print)
        tree_data = self._get_tree_field2string(custom_print, related_field)
        result['header_data'] = header_data
        result['tree_data'] = tree_data
        return result

    def _get_instance_tree_field2value(self,odoo_data,valid_fields):
        '''
        得到待打印单据包含字段名和值的列表字典
        '''
        tree_model = self._get_tree_instance(odoo_data)
        field_attributes = tree_model.fields_get(valid_fields)

        all_res=[]
        for rec in tree_model:
            res = {}
            for field in valid_fields:
                res[field] = self._convert_value(rec, field_attributes, field)
            all_res.append(res)
        return all_res


    def _get_instance_header_field2value(self,odoo_data,valid_fields):
        '''
        得到待打印单据包含字段名和值的表头字典
        '''
        print_model = self._get_print_instance(odoo_data)
        field_attributes=print_model.fields_get(valid_fields)
        res={}
        for field in valid_fields:
            res[field]=self._convert_value(print_model,field_attributes,field)
        return res

    def _get_print_instance(self,odoo_data):
        '''
        得到待打印单据的实例
        '''
        active_id = int(odoo_data.get('print_model_id'))
        print_model = self.env[odoo_data.get('print_model')].browse(active_id)
        return print_model

    def _get_tree_instance(self,odoo_data):
        '''
        得到列表的实例
        '''
        related_field = odoo_data.get('related_field')
        print_model=self._get_print_instance(odoo_data)
        return getattr(print_model, related_field)



    def _get_header_field2string(self, custom_model):
        '''
        得到一个包含字段名和值的表头字典
        '''
        valid_fields =self._filter_header_fileds(custom_model)
        print_model = self.env[custom_model.model_id.model]
        values = print_model.with_context(lang='zh_CN').fields_get(valid_fields, ['string'])

        res = {}
        for key, val in values.items():
            res[key] = _(val['string'])

        return res

    def _get_tree_field2string(self, custom_model, related_field):
        '''
        得到一个包含字段名和值的列表字典
        '''
        print_model = self.env[custom_model.model_id.model]
        tree_model = getattr(print_model, related_field)

        valid_fields = self._filter_tree_fileds(custom_model)

        values = tree_model.with_context(lang='zh_CN').fields_get(valid_fields, ['string'])

        res = {}
        for key, val in values.items():
            res[key] = _(val['string'])

        return res

    def _filter_header_fileds(self,custom_model):
        '''
        得到自定义单据中表头有效的字段
        '''
        return custom_model.header_field_needed_ids.filtered(lambda x:x.is_need==True).mapped('field_id').mapped('name')

    def _filter_tree_fileds(self,custom_model):
        '''
        得到自定义单据中列表有效的字段
        '''
        return custom_model.tree_field_needed_ids.filtered(lambda x:x.is_need==True).mapped('field_id').mapped('name')

    def _get_custom_model(self,odoo_data):
        '''
        得到自定义单据的实例
        '''
        action_type=odoo_data.get('action_type')
        if action_type=='print':
            active_id = int(odoo_data.get('print_model_id'))
            custom_model_name=odoo_data.get('custom_model_name')
            print_model = self.env[odoo_data.get('print_model')].browse(active_id)

            custom_model = self.search([('model_id.model', '=', print_model._name),('name', '=', custom_model_name)])
            return custom_model
        elif action_type=='setting':
            custom_model_id = int(odoo_data.get('custom_model_id'))
            custom_print = self.browse(custom_model_id)
            return custom_print

    def _get_print_model(self,odoo_data):
        '''
        得到自定义单据中待打印单据的模型
        '''
        action_type=odoo_data.get('action_type')
        if action_type=='print':
            active_id = int(odoo_data.get('print_model_id'))
            print_model = self.env[odoo_data.get('print_model')].browse(active_id)
            return print_model


    def _convert_value(self, model, fields_attr, field):
        '''
        将字段值转换成人类能看懂的值
        '''
        field_attr = fields_attr[field]
        value = getattr(model, field)
        if field_attr['type'] == 'selection':
            selection = field_attr['selection']
            res = None
            for s in selection:
                if s[0] == value:
                    res = s[1]
                    break
            return res
        elif field_attr['type'] == 'boolean':
            res = '是' if getattr(model, field) else '否'
            return res

        elif value == False and not isinstance(value, float):
            res = ''
            return res
        elif isinstance(value, models.Model):
            value = value.sorted("id").sudo()
            if value:
                res = getattr(value[0], 'name', '')
                if res=='':
                    res = getattr(value[0], 'display_name', '')
            else:
                res = ""
            return _(res)
        elif isinstance(value, datetime.datetime):
            value += datetime.timedelta(hours=8)
            res = value.strftime("%Y-%m-%d")
            return res
        elif isinstance(value, datetime.date):
            value += datetime.timedelta(hours=8)
            res = value.strftime("%Y-%m-%d")
            return res
        return _(value)


