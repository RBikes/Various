# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.safe_eval import safe_eval
from ast import literal_eval
from openerp.exceptions import Warning

class sale_config_settings(models.Model):
    _inherit = 'sale.config.settings'

    sale_default_template_id = fields.Many2one('email.template', string="Default Template", domain="[('model_id.model', '=', 'sale.order')]")

    def get_default_email_template(self, cr, uid, fields, context=None):
        icp = self.pool.get('ir.config_parameter')
        return {
            'sale_default_template_id': safe_eval(icp.get_param(cr, uid, 'default_email_template.sale_default_template_id', 'False')),
        }

    def set_default_email_template(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids[0], context=context)
        icp = self.pool.get('ir.config_parameter')
        icp.set_param(cr, uid, 'default_email_template.sale_default_template_id', repr(config.sale_default_template_id.id))

class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_quotation_send_default_template(self):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        default_template_value = literal_eval(self.env["ir.config_parameter"].get_param('default_email_template.sale_default_template_id', 'False'))
        if default_template_value:
            template = self.env['email.template'].search([('id','=',default_template_value)])
        else:
            #template = self.env.ref('sale.email_template_edi_sale', False)
            raise Warning("There is no mail template defined. \nPlease Define an Email Template in Settings/Configuration/Sales") 
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict()
        ctx.update({
            'default_model': 'sale.order',
            'default_res_id': self.id,
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

