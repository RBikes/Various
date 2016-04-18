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

from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from openerp.osv import fields, osv
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _
import pytz
from openerp import SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)

class sale_order(osv.osv):
    _inherit = "sale.order"

    def _get_shipped(self, cr, uid, ids, name, args, context=None):
        res = {}
        for sale in self.browse(cr, uid, ids, context=context):

            delivered = True
            count_done = 0
            for pick in sale.picking_ids:
                if pick.state not in ['cancel', 'done']:
                    delivered = False
                if pick.state in ['done']:
                    count_done += 1

            if count_done == 0:
                delivered = False            

            res[sale.id] = delivered
            #res[sale.id] = all([pick.state in ['cancel', 'done'] for pick in sale.picking_ids])

        return res

    _columns = {
        'shipped': fields.function(_get_shipped, type='boolean', string='Delivered'),
# store={'procurement.order': (_get_orders_procurements, ['state'], 10)})
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
