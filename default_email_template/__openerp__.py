# -*- coding: utf-8 -*-
{
    'name': "Default Email Template",
    'summary': """Allows you to select the default e-mail template for sales orders and invoices""",
    'author': "CML,Bitodoo",
    'website': "",
    'category': 'Sales',
    'version': '0.1',
    'depends': [
        'account',
        'sale',
        ],
    'data': [     
        'views/account_invoice_view.xml',
        'views/sale_order_view.xml',
    ],
    'images': [
            'static/description/icon.png',
            ],
    'price': 20,
    'license': 'AGPL-3',
    'currency': 'EUR',
}
