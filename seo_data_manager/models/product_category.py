# -*- coding: utf-8 -*-

from openerp.osv import osv,fields

class product_public_category(osv.Model):
    _inherit = ["product.public.category", "website.seo.metadata"]
    _name = 'product.public.category'
    
    _columns = {
            'not_update_seo_details' : fields.boolean('Not Update SEO Details',default=False),
        }