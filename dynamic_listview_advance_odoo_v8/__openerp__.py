{
    'name': 'Dynamic ListView Advance V8',
    'summary': 'Change The Odoo List view On the fly without any technical knowledge',
    'version': '1.0',
    'category': 'Web',
    'description': """

    """,
    'author': "Strong Apps",
    'website': 'http://www.hanelsoft.vn/',
    'depends': ['web'],
    'data': ['templates.xml',
             'security/show_fields_security.xml',
             'security/ir.model.access.csv'],
    'price': 139.00,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': False,
    'qweb': ['static/src/xml/listview_button_view.xml'],
    'images': [
        'images/4.jpg',
    ],
}
