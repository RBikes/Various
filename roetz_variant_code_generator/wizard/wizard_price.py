# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010-2011 OpenERP S.A. (<http://www.openerp.com>).
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.exceptions import except_orm
import openerp
from openerp.osv import fields, osv
from openerp.tools.translate import _

class wizard_price(osv.osv):
    _name = "wizard.price"
    _description = "Compute cost prices wizard"
    _columns = {
        #'info_field': fields.text('Info', readonly=True), 
        #'real_time_accounting': fields.boolean("Generate accounting entries when real-time"),
        #'recursive': fields.boolean("Change prices of child BoMs too"),
        }

    def compute_from_bom(self, cr, uid, ids, context=None):
        registry = openerp.registry(cr.dbname)
        prod_obj = registry.get('product.template')
        for prod in prod_obj.browse(cr,uid,ids,context=context):
            prod_obj.calc_cost_prices(cr, uid, ids, prod.id, context=context)
        for prod in prod_obj.browse(cr,uid,ids,context=context):
            prod_obj.calc_cost_prices(cr, uid, ids, prod.id, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
