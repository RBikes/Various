# -*- coding: utf-8 -*-
{
    'name': "Link sales order to mfg order",
    'description': """
    """,
    'author': "Roetz-Bikes BV",
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views.xml',
    ],
    'images': [
    ],
}
