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
from openerp.osv import fields, osv, orm
from openerp import tools
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)

class ResPartner(orm.Model):

    _inherit = 'res.partner'

    _columns = {'sepa_id': fields.int('SEPA ID', size = 50),
                #'sepa_int': fields.char('sepa inter', size = 30),
               }

#    def create_sepa_id(self, cr, uid, vals, context=None):
#        context = context or {}
#        mysequence = self.pool.get('ir.sequence').next_by_code(cr, uid, 'res.partner.sepa')
#        vals['sepaID'] = mysequence

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
