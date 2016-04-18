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
import logging
from openerp.osv import fields, osv
from openerp import tools
from openerp import SUPERUSER_ID
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class product_template(osv.osv):

    _inherit = 'product.template'
    _columns = {'sale_delay_not_avail': fields.float('Lead Time Not Available')
               }

    _defaults = {
        'sale_delay': lambda *a: 7,
        'sale_delay_not_avail': lambda *a: 28,
    }

class product_product(osv.osv):

    _inherit = 'product.product'

    def get_sale_delay(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for each in ids:
            product = self.browse(cr,uid,ids,context=context)
            #template_obj = self.pool.get('product.template')
            #template = template_obj.browse(cr,uid,product.product_tmpl_id,context=context)
            #template = template_obj.browse(cr,uid,ids=template_id,context=context)
            if product.virtual_available > 0:
                res[each] = sale_delay
            else:
                res[each] = sale_delay_not_avail
        return res

    _columns = {'sale_delay_dyn': fields.function(get_sale_delay, type="float", digits_compute=dp.get_precision('0 digits'),string="Lead Time"),
               }




        


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
