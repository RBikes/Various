from .Base import *
from openerp.addons.payment_mollie.controllers.Mollie.API.Object import Issuer


class Issuers(Base):

    def getResourceObject(self, result):
        return Issuer(result)
