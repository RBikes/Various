# coding: utf-8
from openerp import api, models
from openerp.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def get_nearest_lang(self, lang):
        """ Overwrite parent method to accomodate different return type of
        get_languages() """
        short = lang.partition('_')[0]
        short_match = False
        for code, name, _lang_obj in request.website.get_languages():
            if code == lang:
                return lang
            if not short_match and code.startswith(short):
                short_match = code
        return short_match
