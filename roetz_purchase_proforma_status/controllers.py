# -*- coding: utf-8 -*-
from openerp import http

# class RoetzPurchaseProformaStatus(http.Controller):
#     @http.route('/roetz_purchase_proforma_status/roetz_purchase_proforma_status/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/roetz_purchase_proforma_status/roetz_purchase_proforma_status/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('roetz_purchase_proforma_status.listing', {
#             'root': '/roetz_purchase_proforma_status/roetz_purchase_proforma_status',
#             'objects': http.request.env['roetz_purchase_proforma_status.roetz_purchase_proforma_status'].search([]),
#         })

#     @http.route('/roetz_purchase_proforma_status/roetz_purchase_proforma_status/objects/<model("roetz_purchase_proforma_status.roetz_purchase_proforma_status"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('roetz_purchase_proforma_status.object', {
#             'object': obj
#         })