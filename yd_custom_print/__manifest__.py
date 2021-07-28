# -*- coding: utf-8 -*-
{
    'name': "Custom Print Designer",

    'summary': """
        自定义打印,可以自己排版绘制打印的格式.666
        """,

    'description': """
        自定义打印,可以自己排版绘制打印的格式.666
    """,

    'author': "316015009@qq.com",
    'website': "http://www.baidu.com",

    'category': 'All',
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
