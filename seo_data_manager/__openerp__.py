# -*- coding: utf-8 -*-

{
    'name': 'Odoo SEO Suite',
    'version': '1.0',
    'author': 'Biztech Consultancy',
    'category': 'Sales',
    'depends': ['website_sale'],
    'website': 'https://www.biztechconsultancy.com/',
    'description': """
This Module is use to add Product Meta Information.
===================================================         
    """,
    'summary': 'Add Meta Details to your Products & Category pages and Optimize your Website Through Odoo SEO Suite.',
    'data': [
             'views/product_metadata_view.xml',
             'wizard/seo_product_template_view.xml',
             'data/product_template.xml'
    ],
    'live_test_url': 'http://odoo.biztechconsultancy.com/web/login?db=app_odoo_seo_suite',
    'images': ['static/description/odoo-seo-suite.png'],
    'price': 59.00,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
