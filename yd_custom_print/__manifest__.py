# -*- coding: utf-8 -*-
{
    'name': "yd_custom_print",

    'summary': """
        可以实现非常好的自定义打印,不用再自己创建表单了.
        """,

    'description': """
        可以实现非常好的自定义打印,不用再自己创建表单了.
    """,

    'author': "make in china",
    'website': "http://www.yidieshuzi.cn",

    'category': '基础',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/custom_print.xml',
        'views/templates.xml',

    ],
    'qweb': [
        "static/src/xml/web_custom_print_btn.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
