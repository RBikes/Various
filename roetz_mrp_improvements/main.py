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

class mrp_production(osv.osv):
    _inherit = 'mrp.production'

    _order = 'name asc'

    _columns={
        'priority2': fields.integer(string='Priority', size=4),
        'material_check': fields.boolean(string='Materials?'),
        'issue': fields.char(string='Issue', size=128),
        'sequence2': fields.integer(string='Sequence', size=4),
        'partner2_id': fields.related('move_prod_id', 'partner_id', 'display_name', type='char', readonly = True, string='Partner')
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
