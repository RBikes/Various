# -*- coding: utf-8 -*-

from openerp import models, fields, api,_
from openerp import exceptions

class product_template(models.Model):
    
    _inherit = 'product.template'
    
    not_update_seo_details = fields.Boolean('Not Update SEO Details',default=False)

class seo_product_template(models.Model):
    
    _name = "seo.product.template"
    
    _description = "SEO Product Template"
    
    name = fields.Char('Name',default='SEO Product Template')
    title = fields.Char('Title')
    keyword = fields.Char('Keyword')
    description =fields.Char('Description')
    separator = fields.Char('Separator',defualt='-')
    multi_separator = fields.Char('Multi Separator',default='-')
    
    @api.cr_uid_ids_context
    def title_validate(self,cr,uid,ids,title,field):
        if title:
            for c in range(0,len(title)):
                if title[c] == '{':
                    sub_str = title[c+1:c+13]
                    if not (sub_str.startswith('Name') or sub_str.startswith('Supplier') or sub_str.startswith('Category') or sub_str.startswith('Description')):
                        raise exceptions.Warning(_('Please check variable name for ' + field + ' and it should be proper as per list.'))
                    if title.find('Name') != -1:
                        index = title.find('Name')
                        if title[index-1] != '{' or title[index+4] != '}':
                            raise exceptions.Warning(_('Please check variable name for ' + field + ' and it should be proper as per list.'))
                    if title.find('Supplier') != -1:
                        index = title.find('Supplier')
                        if title[index-1] != '{' or title[index+8] != '}':
                            raise exceptions.Warning(_('Please check variable name for ' + field + ' and it should be proper as per list.'))
                    if title.find('Category') != -1:
                        index = title.find('Category')
                        if title[index-1] != '{' or title[index+8] != '}':
                            raise exceptions.Warning(_('Please check variable name for ' + field + ' and it should be proper as per list.'))
                    if title.find('Description') != -1:
                        index = title.find('Description')
                        if title[index-1] != '{' or title[index+11] != '}':
                            raise exceptions.Warning(_('Please check variable name for ' + field + ' and it should be proper as per list.'))
            return True
    
    @api.cr_uid_ids_context
    def write(self, cr, uid, ids,data,context=None):
        result = super(seo_product_template, self).write(cr, uid, ids,data, context=context)
        cur_data = self.browse(cr,uid,ids)
        self.title_validate(cr,uid,ids,cur_data.title,'Title')
        self.title_validate(cr,uid,ids,cur_data.keyword,'Keyword')
        self.title_validate(cr,uid,ids,cur_data.description,'Description')
        return result
    
    @api.multi
    def generate_data(self,title,field):
        prod_templ_obj = self.env['product.template']
        prod_temp_rec = prod_templ_obj.search([('not_update_seo_details','=',False)])
        website_setting_obj = self.env['website']
        sep = website_setting_obj.search([])[0]
        multi_sep =  sep.seo_product_multi_separator
        template_sep =  sep.seo_product_separator
        if  title:
            for product in prod_temp_rec:
                meta_title = ''
                for s1 in title.split('{'):
                    s = str(s1)
                    if s.startswith('Name'):
                            meta_title += product.name
                            index = s.find('Name')
                            sub_str = s[index+5:len(s)]
                            meta_title += sub_str
                    elif s.startswith('Supplier'):
                        for sell in product.seller_ids:
                            seller = ''
                            seller += sell.name.name
                            if multi_sep:
                                seller += multi_sep
                            else:
                                seller += '-'
                            meta_title += seller
                        if multi_sep:
                            if meta_title.endswith(multi_sep):
                                cnt = len(meta_title)
                                meta_title = meta_title[:cnt-len(multi_sep)]
                        else:
                            if meta_title.endswith('-'):
                                cnt = len(meta_title)
                                meta_title = meta_title[:cnt-1]
                        index = s.find('Supplier')
                        sub_str = s[index+9:len(s)]
                        meta_title += sub_str
                    elif s.startswith('Category'):
                        if product.public_categ_ids:
                            meta_title += product.public_categ_ids.name
                            index = s.find('Category')
                            sub_str = s[index+9:len(s)]
                            meta_title += sub_str
                    elif s.startswith('Description'):
                        #if product.description_sale:
                        #    meta_title += product.description_sale
                        if product.web_product_description:
                            meta_title += product.web_product_description
                            index = s.find('Description')
                            sub_str = s[index+12:len(s)]
                            meta_title += sub_str
                    else:
                        meta_title += s
                if template_sep:
                    if meta_title.endswith(template_sep):
                        cnt = len(meta_title)
                        meta_title = meta_title[:cnt-len(template_sep)]
                if field == 'title':
                    product.website_meta_title = meta_title
                if field == 'description':
                    product.website_meta_description = meta_title
                if field == 'keyword':
                    product.website_meta_keywords = meta_title
        else:
            for product in prod_temp_rec:
                if field == 'title':
                    product.website_meta_title = ''
                if field == 'description':
                    product.website_meta_description = ''
                if field == 'keyword':
                    product.website_meta_keywords = ''
        return True
    @api.multi
    def generate(self):
        view_ref = self.pool.get('ir.model.data').get_object_reference(self._cr, self._uid, 'seo_data_manager', 'seo_product_success_update_view')
        view_id = view_ref and view_ref[1] or False,
        self.generate_data(self.title,'title')
        self.generate_data(self.keyword,'keyword')
        self.generate_data(self.description,'description')
        if self.title or self.keyword or self.description:
            return {
               'type': 'ir.actions.act_window',
               'name': 'SEO Product Data Updated',
               'view_mode': 'form',
               'view_type': 'form',
               'view_id': view_id,
               'res_model': 'success.update',
               'target':'new',
               'context': self._context,
               }
        if not (self.title or self.keyword or self.description):
            raise exceptions.Warning(_('There is not any update for Product Meta data '))
        return True
          
    
    def get_data(self,cr,uid,ids,context):
        
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'seo_data_manager', 'seo_product_title_detail_view')
        view_id = view_ref and view_ref[1] or False,
        return {
               'type': 'ir.actions.act_window',
               'name': 'Title Details',
               'view_mode': 'form',
               'view_type': 'form',
               'view_id': view_id,
               'res_model': 'seo.title.detail',
               'target':'new',
               'context': context,
    }
        
    def get_keyword_data(self,cr,uid,ids,context):
        
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'seo_data_manager', 'seo_product_keyword_detail_view')
        view_id = view_ref and view_ref[1] or False,
        return {
               'type': 'ir.actions.act_window',
               'name': 'Keyword Details',
               'view_mode': 'form',
               'view_type': 'form',
               'view_id': view_id,
               'res_model': 'seo.keyword.detail',
               'target':'new',
               'context': context,
    }
        
    def get_description_data(self,cr,uid,ids,context):
        
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'seo_data_manager', 'seo_product_description_detail_view')
        view_id = view_ref and view_ref[1] or False,
        return {
               'type': 'ir.actions.act_window',
               'name': 'Description Details',
               'view_mode': 'form',
               'view_type': 'form',
               'view_id': view_id,
               'res_model': 'seo.description.detail',
               'target':'new',
               'context': context,
    }
    
class seo_product_category(models.Model):
    
    _name = "seo.product.category"
    
    _description = "SEO Category Template"
    
    name = fields.Char('Name',default='SEO Category Template')
    title = fields.Char('Title')
    keyword = fields.Char('Keyword')
    description =fields.Char('Description')
    separator = fields.Char('Separator',default='-')
    multi_separator = fields.Char('Multi Separator',default='-')
    
    @api.cr_uid_ids_context
    def title_validate(self,cr,uid,ids,title,field):
        if title:
            for c in range(0,len(title)):
                if title[c] == '{':
                    sub_str = title[c+1:c+13]
                    if not (sub_str.startswith('Name') or sub_str.startswith('Category')):
                        raise exceptions.Warning(_('Please check variable name for ' + field + ' and it should be proper as per list.'))
                    if title.find('Name') != -1:
                        index = title.find('Name')
                        if title[index-1] != '{' or title[index+4] != '}':
                            raise exceptions.Warning(_('Please check variable name for ' + field + ' and it should be proper as per list.'))
                    if title.find('Supplier') != -1:
                        index = title.find('Supplier')
                        if title[index-1] != '{' or title[index+8] != '}':
                            raise exceptions.Warning(_('Please check variable name for ' + field + ' and it should be proper as per list.'))
                    if title.find('Category') != -1:
                        index = title.find('Category')
                        if title[index-1] != '{' or title[index+8] != '}':
                            raise exceptions.Warning(_('Please check variable name for ' + field + ' and it should be proper as per list.'))
                    if title.find('Description') != -1:
                        index = title.find('Description')
                        if title[index-1] != '{' or title[index+11] != '}':
                            raise exceptions.Warning(_('Please check variable name for ' + field + ' and it should be proper as per list.'))
            return True
    
    @api.cr_uid_ids_context
    def write(self, cr, uid, ids,data,context=None):
        result = super(seo_product_category, self).write(cr, uid, ids,data, context=context)
        cur_data = self.browse(cr,uid,ids)
        self.title_validate(cr,uid,ids,cur_data.title,'Title')
        self.title_validate(cr,uid,ids,cur_data.keyword,'Keyword')
        self.title_validate(cr,uid,ids,cur_data.description,'Description')
        return result
    
    @api.multi
    def generate_data(self,title,field):
        prod_templ_obj = self.env['product.public.category']
        prod_temp_rec = prod_templ_obj.search([('not_update_seo_details','=',False)])
        if  title:
            for product in prod_temp_rec:
                meta_title = ''
                for s1 in title.split('{'):
                    s = str(s1)
                    if s.startswith('Name'):
                            meta_title += product.name
                            index = s.find('Name')
                            sub_str = s[index+5:len(s)]
                            meta_title += sub_str
                    elif s.startswith('Category'):
                        if product.parent_id:
                            meta_title += product.parent_id.name
                            index = s.find('Category')
                            sub_str = s[index+9:len(s)]
                            meta_title += sub_str
                    else:
                        meta_title += s
                if field == 'title':
                    product.website_meta_title = meta_title
                if field == 'description':
                    product.website_meta_description = meta_title
                if field == 'keyword':
                    product.website_meta_keywords = meta_title
        else:
            for product in prod_temp_rec:
                if field == 'title':
                    product.website_meta_title = ''
                if field == 'description':
                    product.website_meta_description = ''
                if field == 'keyword':
                    product.website_meta_keywords = ''
        return True
    @api.multi
    def generate(self):
        view_ref = self.pool.get('ir.model.data').get_object_reference(self._cr, self._uid, 'seo_data_manager', 'seo_category_success_update_view')
        view_id = view_ref and view_ref[1] or False,
        self.generate_data(self.title,'title')
        self.generate_data(self.keyword,'keyword')
        self.generate_data(self.description,'description')
        if self.title or self.keyword or self.description:
            return {
               'type': 'ir.actions.act_window',
               'name': 'SEO Category Data Updated',
               'view_mode': 'form',
               'view_type': 'form',
               'view_id': view_id,
               'res_model': 'success.update.category',
               'target':'new',
               'context': self._context,
               }
        if not (self.title or self.keyword or self.description):
            raise exceptions.Warning(_('There is not any update for Product Meta data '))
        return True
    
    def get_data(self,cr,uid,ids,context):
        
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'seo_data_manager', 'seo_product_category_title_detail_view')
        view_id = view_ref and view_ref[1] or False,
        return {
               'type': 'ir.actions.act_window',
               'name': 'Title Details',
               'view_mode': 'form',
               'view_type': 'form',
               'view_id': view_id,
               'res_model': 'seo.category.title.detail',
               'target':'new',
               'context': context,
    }
        
    def get_keyword_data(self,cr,uid,ids,context):
        
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'seo_data_manager', 'seo_product_category_keyword_detail_view')
        view_id = view_ref and view_ref[1] or False,
        return {
               'type': 'ir.actions.act_window',
               'name': 'Keyword Details',
               'view_mode': 'form',
               'view_type': 'form',
               'view_id': view_id,
               'res_model': 'seo.category.keyword.detail',
               'target':'new',
               'context': context,
    }
        
    def get_description_data(self,cr,uid,ids,context):
        
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'seo_data_manager', 'seo_product_category_description_detail_view')
        view_id = view_ref and view_ref[1] or False,
        return {
               'type': 'ir.actions.act_window',
               'name': 'Description Details',
               'view_mode': 'form',
               'view_type': 'form',
               'view_id': view_id,
               'res_model': 'seo.category.description.detail',
               'target':'new',
               'context': context,
    }

class website(models.Model):

    """Adds the fields for SEO Template."""

    _inherit = 'website'
    
    seo_product_separator = fields.Char(string=' Default Template Separator',default='-')
    seo_product_multi_separator = fields.Char(string='Multiple value Separator',default='-')
    is_replace_character = fields.Boolean(string='Do you want to replace the exiting default templates (Category & Product ) separator?')
    
class WebsiteConfigSettings(models.TransientModel):

    """Settings for the Terms and Condition."""

    _inherit = 'website.config.settings'
    
    seo_product_separator = fields.Char(related='website_id.seo_product_separator',
                                        string=' Default Template Separator',
                                        default='-')
    seo_product_multi_separator = fields.Char(
                                              related='website_id.seo_product_multi_separator',
                                              string='Multiple value Separator',
                                              default='-')
    is_replace_character = fields.Boolean(related='website_id.is_replace_character',
                                       string="Do you want to replace the exiting default templates (Category & Product ) separator?")
    
    def execute(self,cr,uid,ids,context=None):
        cur_data = self.browse(cr,uid,ids)
        if cur_data.is_replace_character:
            pro_temp_obj = self.pool.get('seo.product.template')
            search_temp = pro_temp_obj.search(cr,uid,[])[0]
            temp_data = pro_temp_obj.browse(cr,uid,[search_temp])
            
            cur_separator = str(temp_data.separator)
            new_separator = str(cur_data.seo_product_separator)
            if new_separator == 'False':
                new_separator = '-'
            if cur_separator != new_separator:
                new_str = False
                if temp_data.title:
                    title_str = str(temp_data.title)
                    if  temp_data.title.find(cur_separator) != -1:
                        new_str = title_str.replace(cur_separator,new_separator)
                    if new_str:
                        pro_temp_obj.write(cr,uid,[search_temp],{'title':new_str,'separator':new_separator},context=context)
                    else:
                        pro_temp_obj.write(cr,uid,[search_temp],{'title':title_str,'separator':cur_separator},context=context)
                if temp_data.keyword:
                    title_str = str(temp_data.keyword)  
                    if  temp_data.keyword.find(cur_separator) != -1:
                        new_str = title_str.replace(cur_separator,new_separator)
                    if new_str:
                        pro_temp_obj.write(cr,uid,[search_temp],{'keyword':new_str,'separator':new_separator},context=context)
                    else:
                        pro_temp_obj.write(cr,uid,[search_temp],{'keyword':title_str,'separator':cur_separator},context=context)
                if temp_data.description:
                    title_str = str(temp_data.description)
                    if  temp_data.description.find(cur_separator) != -1:
                        new_str = title_str.replace(cur_separator,new_separator)
                    if new_str:
                        pro_temp_obj.write(cr,uid,[search_temp],{'description':new_str,'separator':new_separator},context=context)
                    else:
                        pro_temp_obj.write(cr,uid,[search_temp],{'description':title_str,'separator':cur_separator},context=context)
            pro_temp_obj.write(cr,uid,[search_temp],{'separator':new_separator},context=context)
            pro_temp_obj = self.pool.get('seo.product.category')
            search_categ_temp = pro_temp_obj.search(cr,uid,[])[0]
            temp_data = pro_temp_obj.browse(cr,uid,[search_categ_temp])
            
            cur_separator = str(temp_data.separator)
            new_separator = str(cur_data.seo_product_separator)
            if cur_separator != new_separator:
                new_str = False
                if temp_data.title:
                    title_str = str(temp_data.title)
                    if  temp_data.title.find(cur_separator) != -1:
                        new_str = title_str.replace(cur_separator,new_separator)
                    if new_str:
                        pro_temp_obj.write(cr,uid,[search_categ_temp],{'title':new_str,'separator':new_separator},context=context)
                    else:
                        pro_temp_obj.write(cr,uid,[search_categ_temp],{'title':title_str,'separator':cur_separator},context=context)
                if temp_data.keyword:
                    title_str = str(temp_data.keyword)
                    if  temp_data.keyword.find(cur_separator) != -1:
                        new_str = title_str.replace(cur_separator,new_separator)
                    if new_str:
                        pro_temp_obj.write(cr,uid,[search_categ_temp],{'keyword':new_str,'separator':new_separator},context=context)
                    else:
                        pro_temp_obj.write(cr,uid,[search_categ_temp],{'keyword':title_str,'separator':cur_separator},context=context)
                if temp_data.description:
                    title_str = str(temp_data.description)
                    if  temp_data.description.find(cur_separator) != -1:
                        new_str = title_str.replace(cur_separator,new_separator)
                    if new_str:
                        pro_temp_obj.write(cr,uid,[search_categ_temp],{'description':new_str,'separator':new_separator},context=context)
                    else:
                        pro_temp_obj.write(cr,uid,[search_categ_temp],{'description':title_str,'separator':cur_separator},context=context)
            pro_temp_obj.write(cr,uid,[search_categ_temp],{'separator':new_separator},context=context)    
        res = super(WebsiteConfigSettings,self).execute(cr,uid,ids,context)
    