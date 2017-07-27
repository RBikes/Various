# -*- coding: utf-8 -*-
import werkzeug
import werkzeug.urls
import base64
import requests
import xmlrpclib
from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug


class faq(http.Controller):
    @http.route('/page/faq', type='http', auth="public", website=True)
    def website_faq(self):
        faqs = []
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        faq_obj = request.registry['faq']
        faq_ids = faq_obj.search(cr, uid, [('website_publish', '=', True)], context=context)
        faqs = faq_obj.browse(cr, uid, faq_ids, context=context)
        return request.website.render("website.faq", {'faqs': faqs})
