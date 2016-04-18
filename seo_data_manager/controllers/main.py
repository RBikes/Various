# -*- coding: utf-8 -*-

from openerp import http
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.http import request

class website_sale_prouduct_category(website_sale):
    
    @http.route(['/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', **post):
        response_object = super(website_sale_prouduct_category,self).shop(page,category,search,**post)
        values = response_object.qcontext
        values['main_object'] = values['category']
        return request.website.render("website_sale.products", values)