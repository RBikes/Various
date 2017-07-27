# -*- coding: utf-8 -*-
import Mollie
from openerp.http import request
from openerp import http, _, SUPERUSER_ID
from openerp.addons.website_sale.controllers import main
class MollieController(http.Controller):
    _redirect_url = '/payment/mollie/'

    @http.route('/mollie/api', type='http', auth="public", methods=["GET", "POST"], website=True)
    def mollie_api(self, **post):
        try:
            mollie = Mollie.API.Client()
            mollie.setApiKey(post['api_key'])
            order_id = post['order_id']
            amount = post['amount']
            payment = mollie.payments.create({'amount': amount, 'description': 'Mollie Payment', 'redirectUrl': post['redirectUrl'], 'metadata': {'order_id': order_id}})
            request.session.update({'mollie_payment_id': payment['id']})
            request.session.update({'mollie_api_key': post['api_key']})
            return request.redirect(payment['links']['paymentUrl'])
        except Mollie.API.Error as e:
            request.session.update({'mollieApiError': True})
            return request.redirect("/shop/payment")

    @http.route('/payment/mollie', type='http', auth="public", methods=["GET", "POST"], website=True)
    def Mollie_back(self, **post):
        """ Return from Mollie """
        mollie = Mollie.API.Client()
        mollie.setApiKey(request.session['mollie_api_key'])
        mollie_payment = mollie.payments.get(request.session['mollie_payment_id'])
        request.session.pop('mollie_api_key')
        request.session.pop('mollie_payment_id')
        if mollie_payment['status'] == 'paid':
            reference = mollie_payment['metadata']['order_id']
            post['txn_id'] = request.env['payment.transaction'].search([('reference', '=', reference)]).id
            post['status'] = mollie_payment['status']
            post['reference'] = reference
            request.env['payment.transaction'].sudo().form_feedback(post, 'mollie')
        return request.redirect('/shop/confirmation')

class mollieShop(main.website_sale):

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        """ Payment step. This page proposes several payment means based on available
        payment.acquirer. State at this point :

         - a draft sale order with lines; otherwise, clean context / session and
           back to the shop
         - no transaction in context / session, or only a draft one, if the customer
           did go to a payment.acquirer website but closed the tab without
           paying / canceling
        """
        cr, uid, context = request.cr, request.uid, request.context
        payment_obj = request.registry.get('payment.acquirer')
        sale_order_obj = request.registry.get('sale.order')

        order = request.website.sale_get_order(context=context)

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        shipping_partner_id = False
        if order:
            if order.partner_shipping_id.id:
                shipping_partner_id = order.partner_shipping_id.id
            else:
                shipping_partner_id = order.partner_invoice_id.id

        values = {
            'order': request.registry['sale.order'].browse(cr, SUPERUSER_ID, order.id, context=context)
        }
        values['errors'] = sale_order_obj._get_errors(cr, uid, order, context=context)
        values.update(sale_order_obj._get_website_data(cr, uid, order, context))

        if not values['errors']:
            acquirer_ids = payment_obj.search(cr, SUPERUSER_ID, [('website_published', '=', True), ('company_id', '=', order.company_id.id)], context=context)
            values['acquirers'] = list(payment_obj.browse(cr, uid, acquirer_ids, context=context))
            render_ctx = dict(context, submit_class='btn btn-primary', submit_txt=_('Pay Now'))
            for acquirer in values['acquirers']:
                acquirer.button = payment_obj.render(
                    cr, SUPERUSER_ID, acquirer.id,
                    order.name,
                    order.amount_total,
                    order.pricelist_id.currency_id.id,
                    partner_id=shipping_partner_id,
                    tx_values={
                        'return_url': '/shop/payment/validate',
                    },
                    context=render_ctx)

        if 'mollieApiError' in request.session.keys():
            values['errors'] = [['Invalid API KEY', 'Please Enter right API KEY']]
            request.session.pop('mollieApiError')
        return request.website.render("website_sale.payment", values)
