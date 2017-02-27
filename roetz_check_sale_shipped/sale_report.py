# coding: utf-8
from openerp.osv import orm


class SaleReport(orm.Model):
    _inherit = 'sale.report'

    def _select(self):
        res = super(SaleReport, self)._select()
        return res.replace(
            ', s.shipped, s.shipped::integer as shipped_qty_1', '')

    def _group_by(self):
        res = super(SaleReport, self)._group_by()
        return res.replace(', s.shipped', '')
