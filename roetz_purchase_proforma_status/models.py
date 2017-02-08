# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class roetz_purchase_proforma_status(osv.osv):
    _inherit = "purchase.order"

    _columns = {
        'pf_po_payed': fields.boolean('Pro Forma Payed')
    }



#     name = fields.Char()