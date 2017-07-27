# -*- coding: utf-8 -*-

{
    'name': 'Mollie Payment',
    'category': 'eCommerce',
    'summary': 'Payment Acquirer: MOLLIE Implementation',
    'version': '0.1',
    'description': """Make your transaction through MOLLIE""",
    'author': "DRC Systems India Pvt. Ltd.",
    'depends': ['payment'],
    'data': [
        'views/mollie.xml',
        'views/payment_acquirer.xml',
        'views/res_config_view.xml',
        'data/mollie.xml',
    ],
    'installable': True,
    'currency':'EUR',
    'price':40,
}
