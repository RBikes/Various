import openerp
from openerp import tools, api
from openerp.osv import osv, fields


class faq(osv.Model):
    _name = "faq"
    _description = "FAQ"

    _columns = {
        'name': fields.char('Frequently asked question', size=255,translate=True),
        'answer': fields.html('Answer',translate=True),
        'website_publish': fields.boolean('Publish On Website'),
    }


faq()
