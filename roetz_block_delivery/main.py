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

from openerp.osv import fields, osv
from openerp.tools.float_utils import float_compare, float_round
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
from dateutil import parser
from openerp import SUPERUSER_ID, api
import openerp.addons.decimal_precision as dp
from openerp.addons.procurement import procurement


class stock_picking(osv.osv):
    _inherit= 'stock.picking'

    _columns = {'blocked': fields.boolean('Block Delivery Order'),
                'block_until': fields.datetime('Block Until', required=False, readonly=False, select=True, states={'sent': [('readonly', True)]}, copy=False),
               }

    @api.cr_uid_ids_context
    def do_enter_transfer_details(self, cr, uid, picking, context=None):

        pick = self.pool.get('stock.picking').browse(cr, uid, picking, context=context)
        if pick.blocked:
            if pick.block_until == False:
                raise osv.except_osv(_('Transfer Blocked!'), _('The transfer is blocked, see the notes for a possible reason'))
            else:
                if parser.parse(pick.block_until) > datetime.now():
                    raise osv.except_osv(_('Transfer Blocked!'), _('The transfer is blocked until a specific date, please wait'))
             
        if not context:
            context = {}

        context.update({
            'active_model': self._name,
            'active_ids': picking,
            'active_id': len(picking) and picking[0] or False
        })

        created_id = self.pool['stock.transfer_details'].create(cr, uid, {'picking_id': len(picking) and picking[0] or False}, context)
        return self.pool['stock.transfer_details'].wizard_view(cr, uid, created_id, context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
