# -*- coding: utf-8 -*-

# since this is no standard model.Model class but a http.Controller class the inheritance mechanisms of odoo would not
# work so we have to use classic python inheritance
# import openerp.addons.website_crm.controllers.main as main

from openerp import http, SUPERUSER_ID
from openerp.tools.translate import _
from openerp.http import request
import smtplib
import openerp.addons.website_crm.controllers.main as main



class contactus_extended(main.contactus):
    def create_lead(self, request, values, kwargs):

	sender = values['email_from']
	receivers = ['info@roetz-bikes.nl']
	#header = """From: Roetz Website <no-reply@roetz-bikes.nl> 
	#To: Roetz Infomail <info@roetz-bikes.nl>
	#Subject: Email Website Contactform
	#"""

	message = 'Subject: Roetz-Bikes Contactform | %s\n  \n\nFrom: %s\nE-Mail: %s\nPhone: %s\nCompany: %s\n\nMessage: %s' % (
		values['name'],
		values['contact_name'],
		values['email_from'],
		values['phone'],
		values['partner_name'],
		values['description'],
	)
	try:
   		smtpObj = smtplib.SMTP('localhost')
   		smtpObj.sendmail(sender, receivers, message)         
   		print "Successfully sent email"
	except SMTPException:
   		print "Error: unable to send email"

	return()