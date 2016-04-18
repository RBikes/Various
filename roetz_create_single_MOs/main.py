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

_logger = logging.getLogger(__name__)

class product_template(osv.osv):
    _inherit= 'product.template'

    _columns = {'create_single_MO': fields.boolean('Single piece manufacturing?', help="Set True if mfg orders should be of quantity 1 only"),
               }

class mrp_production(osv.osv):
    _inherit = 'mrp.production'

    _columns = {'procurement_id': fields.many2one('procurement.order','Source Procurement'),
               }


class procurement_order(osv.osv):
    _inherit = 'procurement.order'

    _columns = {'production_ids': fields.one2many('mrp.production','id','Manufacturing Orders'),
               }

    def make_mo(self, cr, uid, ids, context=None):
        """ Make Manufacturing(production) order from procurement
        @return: New created Production Orders procurement wise
        If single piece production, then create nr of orders equal to quantity. (only if uom = 1)
        """
        res = {}
        production_obj = self.pool.get('mrp.production')
        procurement_obj = self.pool.get('procurement.order')
        product_obj = self.pool.get('product.product')
        for procurement in procurement_obj.browse(cr, uid, ids, context=context):
            if self.check_bom_exists(cr, uid, [procurement.id], context=context):
                #create the MO as SUPERUSER because the current user may not have the rights to do it (mto product launched by a sale for example)
                vals = self._prepare_mo_vals(cr, uid, procurement, context=context)

                ### create single MOs if requested ###
                req_qty = vals["product_qty"]
                prod_id = vals["product_id"]
                _logger.warning(prod_id)
                prod_unit = vals["product_uom"]
                prod = product_obj.browse(cr, uid, int(prod_id), context=context)
                if prod.create_single_MO and prod_unit == 1.0:
                    vals["product_qty"] = "1.0"
                    order_list = []
                    for y in range(0, int(req_qty)):
                        produce_id = production_obj.create(cr, SUPERUSER_ID, vals, context=context)
                        res[procurement.id] = produce_id

                        self.write(cr, uid, [procurement.id], {'production_id': produce_id})
                        self.production_order_create_note(cr, uid, procurement, context=context)
                        self.write(cr, uid, [procurement.id], {'production_id': ''})
                        production_obj.write(cr, uid, [produce_id], {'procurement_id': procurement.id})

                        production_obj.action_compute(cr, uid, [produce_id], properties=[x.id for x in procurement.property_ids])
                        production_obj.signal_workflow(cr, uid, [produce_id], 'button_confirm')

                else:  
                    produce_id = production_obj.create(cr, SUPERUSER_ID, vals, context=context)
                    res[procurement.id] = produce_id
                    self.write(cr, uid, [procurement.id], {'production_id': produce_id})
                    self.production_order_create_note(cr, uid, procurement, context=context)
                    self.write(cr, uid, [procurement.id], {'production_id': ''})
                    production_obj.write(cr, uid, [produce_id], {'procurement_id': procurement.id})

                    production_obj.action_compute(cr, uid, [produce_id], properties=[x.id for x in procurement.property_ids])
                    production_obj.signal_workflow(cr, uid, [produce_id], 'button_confirm')  
            else:
                res[procurement.id] = False
                self.message_post(cr, uid, [procurement.id], body=("No BoM exists for this product!"), context=context)
        return res

    def propagate_cancel(self, cr, uid, procurement, context=None):
        production_obj = self.pool.get('mrp.production')
        if procurement.rule_id.action == 'manufacture' and procurement.production_id:
            self.pool.get('mrp.production').action_cancel(cr, uid, [procurement.production_id.id], context=context)
        if procurement.rule_id.action == 'manufacture' and not procurement.production_id:
            prod_orders = production_obj.search(cr, uid, [('procurement_id', '=', procurement.id)], context=context)
            _logger.warning(prod_orders)
            for order in prod_orders:
                production_obj.action_cancel(cr, uid, [order], context=context)
                #order.action_cancel(cr, uid, [production], context=context)
        return super(procurement_order, self).propagate_cancel(cr, uid, procurement, context=context)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
