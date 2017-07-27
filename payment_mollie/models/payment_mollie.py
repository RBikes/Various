# -*- coding: utf-'8' "-*-"
import logging
from openerp.addons.payment.models.payment_acquirer import ValidationError
from openerp.addons.payment_mollie.controllers.main import MollieController
from openerp.osv import osv, fields
import urlparse
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)


class AcquirerMollie(osv.Model):
    _inherit = 'payment.acquirer'

    def _get_mollie_urls(self, cr, uid, environment, context=None):
        """ Mollie URLS """
        if environment == 'prod':
            return {
                'mollie_form_url': '/mollie/api',
            }
        else:
            return {
                'mollie_form_url': '/mollie/api',
            }

    def _get_providers(self, cr, uid, context=None):
        providers = super(AcquirerMollie, self)._get_providers(cr, uid, context=context)
        providers.append(['mollie', 'Mollie'])
        return providers

    _columns = {
        'api_key': fields.char('Secret Key', required_if_provider='mollie'),
    }

    def mollie_get_form_action_url(self, cr, uid, id, context=None):
        acquirer = self.browse(cr, uid, id, context=context)
        return self._get_mollie_urls(cr, uid, acquirer.environment, context=context)['mollie_form_url']

    def mollie_form_generate_values(self, cr, uid, id, partner_values, tx_values, context=None):
        base_url = self.pool['ir.config_parameter'].get_param(cr, SUPERUSER_ID, 'web.base.url')
        acquirer = self.browse(cr, uid, id, context=context)
        sale_order = tx_values['reference'],
        sale_order = sale_order[0]
        mollie_tx_values = dict(tx_values)
        mollie_tx_values.update({
            'api_key': acquirer.api_key,
            'amount': tx_values['amount'],
            'description': 'Mollie Payment',
            'redirectUrl': '%s' % urlparse.urljoin(base_url, MollieController._redirect_url),
            'order_id': sale_order,
            'locale': 'en',
            # 'webhookUrl': '%s' % urlparse.urljoin(base_url, MollieController._webhook_url),
        })
        return partner_values, mollie_tx_values

class TxMollie(osv.Model):
    _inherit = 'payment.transaction'

    _columns = {
        'mollie_txn_id': fields.char('Transaction ID'),
        'mollie_txn_type': fields.char('Transaction type'),
    }

    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------

    def _mollie_form_get_tx_from_data(self, cr, uid, data, context=None):
        reference = data.get('reference')
        tx_ids = self.pool['payment.transaction'].search(cr, uid, [('reference', '=', reference)], context=context)
        if not tx_ids or len(tx_ids) > 1:
            error_msg = 'Mollie: received data for reference %s' % (reference)
            if not tx_ids:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.error(error_msg)
            raise ValidationError(error_msg)

        return self.browse(cr, uid, tx_ids[0], context=context)

    def _mollie_form_validate(self, cr, uid, tx, data, context=None):
        if data['status'] == 'paid':
            self.write(cr, uid, tx.id, {'state': 'done'}, context=context)
            return True
        else:
            self.write(cr, uid, tx.id, {'state': 'error'}, context=context)
            return False
