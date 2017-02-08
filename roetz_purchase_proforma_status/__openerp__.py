# -*- coding: utf-8 -*-
{
    'name': "roetz_purchase_proforma_status",

    'summary': """
        Keep track of Proforma invoice payment status for purchasing""",

    'description': """

    """,

    'author': "Roetz-Bikes BV",
    'website': "http://roetz-bikes.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}