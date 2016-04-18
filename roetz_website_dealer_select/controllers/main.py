from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

import logging
from openerp import http
from openerp.http import request
#import openerp.addons.website_sale.controllers.main

_logger = logging.getLogger(__name__)

class main(http.Controller):

    @http.route(['/shop/nearby_dealers'], type='json', auth="public")
    def nearby_dealers(self, distance=None, lat=None, lng=None, **post):
        offset = 0
        limit = 500

        request.cr.execute('''SELECT
                res_partner.id,
                res_partner.display_name as name,
                res_partner.street,
                res_partner.zip,
                res_partner.city,
                res_partner.phone,
                res_partner.website,
                res_partner.country_id,
                res_partner.partner_latitude as lat,
                res_partner.partner_longitude as lng,
                earth_distance(ll_to_earth( '%s','%s' ), ll_to_earth(res_partner.partner_latitude, res_partner.partner_longitude)) as distance           
            FROM res_partner
            WHERE res_partner.active=True
            AND res_partner.grade_id=2
            ORDER BY distance
            LIMIT %s OFFSET %s''', (lat, lng, limit, offset))

        result = request.cr.dictfetchall()

        if not result:
            return {'error':'query failed'}

        dealers = []

        for dealer in result:
            dealers.append(dealer)

        return dealers
