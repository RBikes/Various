# -*- coding: utf-8 -*-

from openerp.osv import orm, fields
from openerp import SUPERUSER_ID
from openerp.addons import decimal_precision

class SaleOrder(orm.Model):
    _inherit = 'sale.order'

    def _amount_all_wrapper(self, cr, uid, ids, field_name, arg, context=None):        
        """ Wrapper because of direct method passing as parameter for function fields """
        return self._amount_all(cr, uid, ids, field_name, arg, context=context)

    
