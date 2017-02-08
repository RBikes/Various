# -*- coding: utf-8 -*-

{
    'name': 'WKR Transfer Payment Acquirer',
    'category': 'Hidden',
    'summary': 'Payment Acquirer: WKR Transfer Implementation',
    'version': '1.0',
    'description': """WKR Transfer Payment Acquirer""",
    'author': 'Roetz-Bikes BV',
    'depends': ['payment'],
    'data': [
        'views/transfer.xml',
        'data/transfer.xml',
    ],
    'installable': True,
    'auto_install': False,
}
