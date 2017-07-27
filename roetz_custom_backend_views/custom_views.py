# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import openerp
from openerp.osv import fields, osv
from openerp import SUPERUSER_ID

### Sort Delivery Orders by Scheduled Date ###
class stock_picking(osv.Model):
    _inherit = 'stock.picking'
    _order = 'min_date asc'

### Purchase Orders: Make Supplier Reference editable in all states ###
class purchase_order(osv.Model):
    _inherit = 'purchase.order'

    _columns = {
        'partner_ref': fields.char('Supplier Reference', states={'confirmed':[('readonly',False)],
                                                                 'approved':[('readonly',True)],
                                                                 'done':[('readonly',True)]},
                                   copy=False,
                                   help="Reference of the sales order or bid sent by your supplier. "
                                        "It's mainly used to do the matching when you receive the "
                                        "products as this reference is usually written on the "
                                        "delivery order sent by your supplier."),
      }



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
