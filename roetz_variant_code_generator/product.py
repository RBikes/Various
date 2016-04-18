# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import pytz
import time
from time import gmtime, strftime
import openerp
from openerp import tools
from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
import os
import logging
from datetime import datetime
import base64
import urllib
import psycopg2
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class product_attribute_sequence(osv.osv):

    _inherit = 'product.attribute.line'
    _order = 'sequence'
    _columns = {'sequence': fields.integer('Sequence', help="Determine the display order"),
               }

class product_attribute_value(osv.osv):
    
    _inherit = 'product.attribute.value'
    _columns = {'att_value_code': fields.char('Attribute Value Code', size=6, help="Max Size = 6 characters"),
                'image_sequence': fields.integer('Image Sequence', default='1', help="Determines in what order attribute images are stacked"),
                'parent_attr_value': fields.many2one('product.attribute.value', 'Parent Attr. Value'),
		  }

#    _sql_constraints = [
#      ('uniq_default_code', 'unique(default_code)', "Reference code must be unique!"),
#	]


class product_template(osv.osv):

    _inherit= 'product.template'

    def create_variant_ids(self, cr, uid, ids, context=None):
        product_obj = self.pool.get("product.product")
        attr_val_obj = self.pool.get("product.attribute.value")
        ctx = context and context.copy() or {}

        if ctx.get("create_product_variant"):
            return None

        ctx.update(active_test=False, create_product_variant=True)

        tmpl_ids = self.browse(cr, uid, ids, context=ctx)
        for tmpl_id in tmpl_ids:

            # list of values combination
            variant_alone = []
            all_variants = [[]]
            for variant_id in tmpl_id.attribute_line_ids:
                if len(variant_id.value_ids) == 1:
                    variant_alone.append(variant_id.value_ids[0])
                temp_variants = []
                for variant in all_variants:
                    _logger.warning(variant)
                    for value_id in variant_id.value_ids:
                        if value_id.parent_attr_value.id:
                            _logger.warning(variant)
                            _logger.warning(value_id.parent_attr_value.id)
                            if value_id.parent_attr_value.id in variant:
                                temp_variants.append(variant + [int(value_id)])
                            else:
                                continue
                        else:
                            temp_variants.append(variant + [int(value_id)])
                all_variants = temp_variants
                _logger.warning(all_variants)

            # adding an attribute with only one value should not recreate product
            # write this attribute on every product to make sure we don't lose them
            for variant_id in variant_alone:
                product_ids = []
                for product_id in tmpl_id.product_variant_ids:
                    if variant_id.id not in map(int, product_id.attribute_value_ids):
                        product_ids.append(product_id.id)
                product_obj.write(cr, uid, product_ids, {'attribute_value_ids': [(4, variant_id.id)]}, context=ctx)

            # check product
            variant_ids_to_active = []
            variants_active_ids = []
            variants_inactive = []
            for product_id in tmpl_id.product_variant_ids:
                variants = map(int,product_id.attribute_value_ids)
                if variants in all_variants:
                    variants_active_ids.append(product_id.id)
                    all_variants.pop(all_variants.index(variants))
                    if not product_id.active:
                        variant_ids_to_active.append(product_id.id)
                else:
                    variants_inactive.append(product_id)
            if variant_ids_to_active:
                product_obj.write(cr, uid, variant_ids_to_active, {'active': True}, context=ctx)

            # create new product
            for variant_ids in all_variants:
                values = {
                    'product_tmpl_id': tmpl_id.id,
                    'attribute_value_ids': [(6, 0, variant_ids)]
                }
                id = product_obj.create(cr, uid, values, context=ctx)
                variants_active_ids.append(id)

            # unlink or inactive product
            for variant_id in map(int,variants_inactive):
                try:
                    with cr.savepoint():
                        product_obj.unlink(cr, uid, [variant_id], context=ctx)
                except (psycopg2.Error, osv.except_osv):
                    product_obj.write(cr, uid, [variant_id], {'active': False}, context=ctx)
                    pass
        return True

    def generate_codes(self, cr, uid, ids, name, arg=None, context=None):

        template = self.browse(cr,uid,ids,context=context)
        tmpl_id = template.id

        #_logger.warning("HET AANTAL VARIANTEN IS %d" % test ) 

        product_ids = self.pool.get('product.product').search(cr, uid, [('product_tmpl_id', '=', tmpl_id)])
        for product in self.pool.get('product.product').browse(cr, uid, product_ids):
            code_str = template.variant_main_code
            prodID = product.id
            for v in product.attribute_value_ids:
                if v.att_value_code == False:
                    code_str = code_str 
                else:
                    code_str = code_str + v.att_value_code
            product.write({"default_code":code_str})

    def generate_EAN_codes(self, cr, uid, ids, arg=None, context=None):

        template = self.browse(cr,uid,ids,context=context)
        tmpl_id = template.id

        product_ids = self.pool.get('product.product').search(cr, uid, [('product_tmpl_id', '=', tmpl_id)])
        for product in self.pool.get('product.product').browse(cr, uid, product_ids):
            product.generate_ean13()

    def generate_images(self, cr, uid, ids, name, arg=None, context=None):
        #filedir ="/opt/roetz-pic/data/pic-assets/generated/variant"
        template_obj = self.browse(cr,uid,ids,context=context)
        template = '"' + template_obj.name + '"'
        database = cr.dbname
        command = '/opt/roetz-pic/roetz-pic.phar composite --db-driver=%s --save-disk --product=%s' %(database, template)
        _logger.warning(command)
        os.system(command)

        tmpl_id = template_obj.id
        product_ids = self.pool.get('product.product').search(cr, uid, [('product_tmpl_id', '=', tmpl_id)])
        for product in self.pool.get('product.product').browse(cr, uid, product_ids):
            #filename = filedir + "/" + template_obj.name + "/" + product.default_code + ".png"
            product.write({"link":True})

    def calc_cost_prices(self, cr, uid, ids, prod, context=None):
        #_logger.warning(template.name)
        registry = openerp.registry(cr.dbname)
        template_pool = registry.get('product.template')
        product_pool = registry.get('product.product')
        bom_pool = registry.get('mrp.bom')
        #if not prod == None:
        #    template = template_pool.browse(cr,uid,ids,context=context)
        #else:
        template = self.browse(cr,uid,ids,context=context)
        tmpl_id = template.id
        #_logger.warning(template.name)
        #bom_obj = self.pool.get('mrp.bom')
        #bom_id = bom_pool.search(cr, uid, [('product_id','=',tmpl_id)], context=context)
        #if bom_id != None:
        if template.cost_price_variable:
                product_ids = product_pool.search(cr, uid, [('product_tmpl_id', '=', tmpl_id)])
                for product in product_pool.browse(cr, uid, product_ids):
                    product.update_cost_prices_product(method='variable')
                template.write({"cost_price_update":strftime("%Y-%m-%d %H:%M:%S", gmtime())})
        else:
                product_ids = product_pool.search(cr, uid, [('product_tmpl_id', '=', tmpl_id)])
                prod_id = product_ids[0]
                product = product_pool.browse(cr, uid, prod_id)
                product.update_cost_prices_product(method='static')
                template.write({"cost_price_update":strftime("%Y-%m-%d %H:%M:%S", gmtime())})

    def get_multi_variant(self, cr, uid, ids, name, arg=None, context=None):
        return self.get_multi_variant_impl(cr, uid, ids, name, arg, context=context)

    def get_multi_variant_impl(self, cr, uid, ids, name, arg=None, context=None):
        #templ_ojb = self.pool.get('product.template')
        template = self.browse(cr,uid,ids,context=context)
        _logger.warning(template.name)
        if len(template.product_variant_ids) > 1:
            return True
        else:
            return False

    _columns = {'variant_main_code': fields.char('Variant Main Code', size=12, help="The leading code for this product template"),
                'cost_price_update': fields.datetime('Last Update'),
                'calculated_cost_price': fields.float('Calculated Price'),
                'kanban_nr': fields.integer('Kanban Nr'),
                'cost_price_variable': fields.boolean('Cost Price Variable?', help="Set True if cost price varies per variant"),
                'web_product_description': fields.text('Web Product Description',translate=True, help="Description of the product as shown on website"),
                'product_specs': fields.text('Product Specification',translate=True, help="Specifications of the product as shown on website"),
               }			               
    _defaults = {'kanban_nr' : '0',
                }

class product_product(osv.osv):

    _inherit = 'product.product'

    def name_get(self, cr, user, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if not len(ids):
            return []

        def _name_get(d):
            name = d.get('name','')
            code = context.get('display_default_code', True) and d.get('default_code',False) or False
            if code:
                #name = '[%s] %s' % (code,name)
                name = '%s | %s' % (code,name)
            return (d['id'], name)

        partner_id = context.get('partner_id', False)
        if partner_id:
            partner_ids = [partner_id, self.pool['res.partner'].browse(cr, user, partner_id, context=context).commercial_partner_id.id]
        else:
            partner_ids = []

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights(cr, user, "read")
        self.check_access_rule(cr, user, ids, "read", context=context)

        result = []
        for product in self.browse(cr, SUPERUSER_ID, ids, context=context):
            # variant = ", ".join([v.name for v in product.attribute_value_ids])
            # name = variant and "%s (%s)" % (product.name, variant) or product.name
            name = product.name
            sellers = []
            if partner_ids:
                sellers = filter(lambda x: x.name.id in partner_ids, product.seller_ids)
            if sellers:
                for s in sellers:
                    # seller_variant = s.product_name and "%s (%s)" % (s.product_name, variant) or False
                    seller_variant = s.product_name and "%s"  %(s.product_name) or False
                    mydict = {
                              'id': product.id,
                              'name': seller_variant or name,
                              'default_code': s.product_code or product.default_code,
                              }
                    result.append(_name_get(mydict))
            else:
                mydict = {
                          'id': product.id,
                          'name': name,
                          'default_code': product.default_code,
                          }
                result.append(_name_get(mydict))
        return result

    def name_get_long(self, cr, user, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if not len(ids):
            return []

        def _name_get(d):
            name = d.get('name','')
            code = context.get('display_default_code', True) and d.get('default_code',False) or False
            if code:
                #name = '[%s] %s' % (code,name)
                name = '%s | %s' % (code,name)
                #name = '%s' % (name)
            return (d['id'], name)

        partner_id = context.get('partner_id', False)
        if partner_id:
            partner_ids = [partner_id, self.pool['res.partner'].browse(cr, user, partner_id, context=context).commercial_partner_id.id]
        else:
            partner_ids = []

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights(cr, user, "read")
        self.check_access_rule(cr, user, ids, "read", context=context)

        result = []
        for product in self.browse(cr, SUPERUSER_ID, ids, context=context):
            variant = ", ".join([v.name for v in product.attribute_value_ids])
            name = variant and "%s (%s)" % (product.name, variant) or product.name
            #name = product.name
            sellers = []
            if partner_ids:
                sellers = filter(lambda x: x.name.id in partner_ids, product.seller_ids)
            if sellers:
                for s in sellers:
                    seller_variant = s.product_name and "%s (%s)" % (s.product_name, variant) or False
                    mydict = {
                              'id': product.id,
                              'name': seller_variant or name,
                              'default_code': s.product_code or product.default_code,
                              }
                    result.append(_name_get(mydict))
            else:
                mydict = {
                          'id': product.id,
                          'name': name,
                          'default_code': product.default_code,
                          }
                result.append(_name_get(mydict))
        return result


    def update_cost_prices_product(self, cr, uid, ids, method, context=None):
		#_logger.warning("FUNCTIE WORDT GEBRUIKT")
		number = 1 #(datas.get('form', False) and datas['form']['number']) or 1
		registry = openerp.registry(cr.dbname)
		product_pool = registry.get('product.product')
		product_uom_pool = registry.get('product.uom')
		workcenter_pool = registry.get('mrp.workcenter')
		user_pool = registry.get('res.users')
		bom_pool = registry.get('mrp.bom')
		byprod_pool = registry.get('mrp.subproduct')
		pricelist_pool = registry.get('product.pricelist')
		company_currency = user_pool.browse(cr, uid, uid).company_id.currency_id
		company_currency_symbol = company_currency.symbol or company_currency.name
		master_prod=self.browse(cr, SUPERUSER_ID, ids, context=context)

		def process_bom(bom, currency_id, factor=1):
			sum = 0
			sum_strd = 0
			prod = product_pool.browse(cr, uid, bom['product_id'])

			prod_qtty = factor * bom['product_qty']
			product_uom = product_uom_pool.browse(cr, uid, bom['product_uom'], context=context)
			main_sp_price, main_sp_name , main_strd_price = '','',''
			sellers, sellers_price = '',''

			if prod.seller_id:
				pricelist =  prod.seller_id.property_product_pricelist_purchase
				price = pricelist_pool.price_get(cr,uid,[pricelist.id],
					prod.id, number*prod_qtty or 1.0, prod.seller_id.id, {
				'uom': prod.uom_po_id.id,
				'date': time.strftime('%Y-%m-%d'),
				})[pricelist.id]
				sum += prod_qtty*price
			#else:
			#	raise osv.except_osv(_('Warning!'), _('Supplier not provided for %s' %prod.name))
			if prod.cost_price_variable:
				std_price = product_uom_pool._compute_price(cr, uid, prod.uom_id.id, prod.variant_cost_price, to_uom_id=product_uom.id)
			else:
				std_price = product_uom_pool._compute_price(cr, uid, prod.uom_id.id, prod.standard_price, to_uom_id=product_uom.id)
			main_strd_price = str(std_price) + '\r\n'
			sum_strd = prod_qtty*std_price
			for seller_id in prod.seller_ids:
				if seller_id.name.id == prod.seller_id.id:
					continue
				pricelist = seller_id.name.property_product_pricelist_purchase
				price = pricelist_pool.price_get(cr,uid,[pricelist.id],
					 prod.id, number*prod_qtty or 1.0, seller_id.name.id, {
						'uom': prod.uom_po_id.id,
						'date': time.strftime('%Y-%m-%d'),
						})[pricelist.id]         
			return sum, sum_strd

		def process_workcenter(wrk):
			workcenter = workcenter_pool.browse(cr, uid, wrk['workcenter_id'])
			cost_cycle = wrk['cycle']*workcenter.costs_cycle
			cost_hour = wrk['hour']*workcenter.costs_hour
			total = cost_cycle + cost_hour
			return total

		for product in product_pool.browse(cr, uid, ids, context=context):
			bom_id = bom_pool._bom_find(cr, uid, product_id=product.id, context=context)
			if not bom_id:
				total_strd = number * product.standard_price
				total = number * product_pool.price_get(cr, uid, [product.id], 'standard_price')[product.id]
							  
			else:
				bom = bom_pool.browse(cr, uid, bom_id, context=context)
				factor = number * product.uom_id.factor / bom.product_uom.factor
				sub_boms = bom_pool._bom_explode(cr, uid, bom, product, factor / bom.product_qty, context=context)
				total = 0
				total_strd = 0
				parent_bom = {
						'product_qty': bom.product_qty,
						'name': bom.product_id.name,
						'product_uom': bom.product_uom.id,
						'product_id': bom.product_id.id
				}
				for sub_bom in (sub_boms and sub_boms[0]) or [parent_bom]:
					sum, sum_strd = process_bom(sub_bom, company_currency.id)
					total += sum
					total_strd += sum_strd

				total2 = 0
				for wrk in (sub_boms and sub_boms[1]):
					sum = process_workcenter(wrk)
					total2 += sum

			if total2:
				super_total = total_strd + total2
			else:
				super_total = total_strd
			#_logger.warning("PRODUCT IS %d" %master_prod)
			#_logger.warning("KOSTPRIJS IS %f" %super_total)
			if method == 'variable':
				master_prod.write({"variant_cost_price":super_total,"cost_price_update":strftime("%Y-%m-%d %H:%M:%S", gmtime())})
			if method == 'static':
				master_prod.write({"standard_price":super_total,"cost_price_update":strftime("%Y-%m-%d %H:%M:%S", gmtime())})


    ### Image generation and links ###

    #def get_image_variant(self, cr, uid, ids, field_name, arg, context={}):
    def _get_image_variant(self, cr, uid, ids, name, args, context=None):
        #_logger.warning("IMAGE WORDT OPGEZOCHT")
        filedir ="/opt/roetz-pic/data/pic-assets/generated/variant"
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.link:
                try:
                    filenametest = filedir + "/" + obj.name_template + "/" + obj.default_code + ".jpg"
                    if os.path.isfile(filenametest):
                        filename = filenametest
                    else:
                        filename = filedir + "/" + obj.name_template + "/" + obj.default_code + ".png"   
                    f = open(filename, 'rb')
                    img = base64.encodestring(f.read())
                    f.close()
                except:
                    img = ''
                result [obj.id] = img
            else:
                result[obj.id] = obj.image_variant or getattr(obj.product_tmpl_id, name)
        return result

    def _set_image_variant(self, cr, uid, id, name, value, args, context=None):
        image = tools.image_resize_image_big(value)
        res = self.write(cr, uid, [id], {'image_variant': image}, context=context)
        product = self.browse(cr, uid, id, context=context)
        if not product.product_tmpl_id.image:
            product.write({'image_variant': None})
            product.product_tmpl_id.write({'image': image})
        return res


    _columns = {'cost_price_update': fields.datetime('Last Update'),
                'variant_cost_price': fields.float('Variant Price'),
                'link': fields.boolean('Link?',
                               help="""Link image to file on disk"""),

        # image: all image fields are base64 encoded and PIL-supported
        'image_variant': fields.binary("Variant Image",
            help="This field holds the image used as image for the product variant, limited to 1024x1024px."),

        'image': fields.function(_get_image_variant, fnct_inv=_set_image_variant,
            string="Big-sized image", type="binary",
            help="Image of the product variant (Big-sized image of product template if false). It is automatically "\
                 "resized as a 1024x1024px image, with aspect ratio preserved."),
        'image_small': fields.function(_get_image_variant, fnct_inv=_set_image_variant,
            string="Small-sized image", type="binary",
            help="Image of the product variant (Small-sized image of product template if false)."),
        'image_medium': fields.function(_get_image_variant, fnct_inv=_set_image_variant,
            string="Medium-sized image", type="binary",
            help="Image of the product variant (Medium-sized image of product template if false)."),
               }			

#    _sql_constraints = [
#      ('uniq_int_reference', 'unique(internal_reference)', "Reference code must be unique!"),
#	]

				
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
