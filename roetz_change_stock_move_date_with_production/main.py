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

class mfg_stock_move_change(osv.osv):
    _inherit = 'mrp.production'

    def on_change_mfg_plan_date(self,cr,uid,ids,date_planned,context=None):
	#Change all planned stock moves related to the manufacturing order
        mfg_order = self.browse(cr, uid, ids, context=context)
        #plan_date = mfg_order.date_planned
        moves_to_change = []
        _logger.warning("Changing planned stock move dates to mfg order date")
        # change planned dates on products to be consumed
        moves_to_change.append(mfg_order.move_lines)
        # change planned dates on products to be produced  
        moves_to_change.append(mfg_order.move_created_ids)
        _logger.warning(moves_to_change)

        #for move in self.pool.get('stock.move').browse(cr, uid, moves_to_change):
        for move in moves_to_change:
            move.write({"date_expected":date_planned,"date":date_planned})
            


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
