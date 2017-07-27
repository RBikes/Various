# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.depends('state', 'move_lines.state')
    def _show_buttons(self):
        for mo in self.filtered(lambda x: x.state not in
                                ('draft', 'cancel', 'done')):
            moves = mo.move_lines.filtered(
                lambda x: x.state in ('waiting', 'confirmed'))
                # lambda x: x.state in ('waiting', 'confirmed') and
                # x.work_order.state not in ('cancel', 'done'))
            mo.show_check_availability = moves
            mo.show_force_reservation = moves

    @api.depends('move_lines.state')
    def _show_unreserve(self):
        for mo in self:
            mo.show_unreserve = mo.move_lines.filtered(
                lambda x: x.state == 'assigned')
                # lambda x: x.state == 'assigned' and
                # x.work_order.state not in ('cancel', 'done'))

    show_check_availability = fields.Boolean(
        string='Show check availability button', compute='_show_buttons')
    show_force_reservation = fields.Boolean(
        string='Show force reservation button', compute='_show_buttons')
    show_unreserve = fields.Boolean(
        string='Show unreserve button', compute='_show_unreserve')

    @api.multi
    def button_unreserve(self):
        moves = self.move_lines.filtered(
            lambda x: x.state == 'assigned')
            # lambda x: x.state == 'assigned' and
            # x.work_order.id == self.id)
        return moves.do_unreserve()
