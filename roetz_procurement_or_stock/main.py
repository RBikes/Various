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

from datetime import date, datetime
from dateutil import relativedelta
import json
import time

import openerp
from openerp.osv import fields, osv
from openerp.tools.float_utils import float_compare, float_round
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from openerp import SUPERUSER_ID, api
import openerp.addons.decimal_precision as dp
from openerp.addons.procurement import procurement
import logging

_logger = logging.getLogger(__name__)


class stock_move(osv.osv):
    _inherit = 'stock.move'

    def product_avail_by_location(self, cr, uid, product_id, warehouse_stock_location, context=None):
        sql = """select ((select sum(product_qty) from stock_move where product_id = %s and state not in ('draft','cancel') and location_dest_id = %s group by product_id) - (select sum(product_qty) from stock_move where product_id = %s and state not in ('draft','cancel') and location_id = %s group by product_id) ) as total;""" % (product_id, warehouse_stock_location, product_id, warehouse_stock_location)
        cr.execute(sql)
        return cr.fetchall()[0][0]

    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirms stock move or put it in waiting if it's linked to another move.
        @return: List of ids.
        """
        if isinstance(ids, (int, long)):
            ids = [ids]
        states = {
            'confirmed': [],
            'waiting': []
        }
        to_assign = {}
        for move in self.browse(cr, uid, ids, context=context):
            self.attribute_price(cr, uid, move, context=context)
            state = 'confirmed'
            #if the move is preceeded, then it's waiting (if preceeding move is done, then action_assign has been called already and its state is already available)
            if move.move_orig_ids:
                state = 'waiting'
            #if the move is split and some of the ancestor was preceeded, then it's waiting as well
            elif move.split_from:
                move2 = move.split_from
                while move2 and state != 'waiting':
                    if move2.move_orig_ids:
                        state = 'waiting'
                    move2 = move2.split_from
            states[state].append(move.id)

            if not move.picking_id and move.picking_type_id:
                key = (move.group_id.id, move.location_id.id, move.location_dest_id.id)
                if key not in to_assign:
                    to_assign[key] = []
                to_assign[key].append(move.id)

        # Overwrite default procurement creation method to check for stock first
        # If available stock quantity of product >= required, set method take from stock. Else set method make to order and create procurement
        for move in self.browse(cr, uid, states['confirmed'], context=context):
            #if move.procure_method == 'make_to_stock':
            move.procure_method = 'make_to_stock'
            if move.location_id.usage == 'internal':
                #available = move.product_avail_by_location(move.product_id.id, move.location_id.id)
                available = move.product_id.virtual_available
                #_logger.warning(move.location_id.complete_name)
                #_logger.warning(move.product_id.name)
                #_logger.warning(available)
                #_logger.warning(move.availability)
                if available < move.product_uom_qty:
                #if move.availability < move.product_uom_qty:
                    if not move.product_id.type == 'consu': ## If product is not consumable:
                        if not move.product_id.orderpoint_ids: ## If product has no minimum stock rules at all, set MTO
                            move.procure_method = 'make_to_order'
                        else: ## Check if there is a stock rule for the source location. If not, set MTO
                            for OP in move.product_id.orderpoint_ids:
                                if OP.location_id != move.location_id:
                                    move.procure_method = 'make_to_order'     

                       
            if move.procure_method == 'make_to_order':
                #moves = [move for move in self.browse(cr, uid, states['confirmed'], context=context) if move.procure_method == 'make_to_order']
                self._create_procurement(cr, uid, move, context=context)
                states['waiting'].append(move.id)
                states['confirmed'].remove(move.id)


        for state, write_ids in states.items():
            if len(write_ids):
                self.write(cr, uid, write_ids, {'state': state})
        #assign picking in batch for all confirmed move that share the same details
        for key, move_ids in to_assign.items():
            procurement_group, location_from, location_to = key
            self._picking_assign(cr, uid, move_ids, procurement_group, location_from, location_to, context=context)
            self.action_assign(cr, uid, move_ids, context=context)
        moves = self.browse(cr, uid, ids, context=context)
        self._push_apply(cr, uid, moves, context=context)
        return ids


#    _columns = {
#        'procure_method': fields.selection([('make_to_stock', 'Default: Take From Stock'), ('make_to_order', 'Create Procurement'), ('check_stock_then procure', 'Check for stock then create Procurement')], 'Supply Method', required=True, 
#                                           help="""By default, the system will take from the stock in the source location and passively wait for availability. The other possibility allows you to directly create a procurement on the source location (and thus ignore its current stock) to gather products. If we want to chain moves and have this one to wait for the previous, this second option should be chosen."""),
#    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
