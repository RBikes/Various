from .Base import *
from openerp.addons.payment_mollie.controllers.Mollie.API.Object import Method


class Methods(Base):

    def getResourceObject(self, result):
        return Method(result)
