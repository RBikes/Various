
# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class title_detail(osv.osv):
    
    _name = "seo.title.detail"
    
    _description = "SEO Title Details"
    
    _columns = {
                
            'name' : fields.boolean('Name'),
            'supplier' : fields.boolean('Supplier Name'),
            'category' : fields.boolean('Category Name'),
            'description' : fields.boolean('Description For Quotation')
    }
    
    def get_title_detail(self,cr,uid,ids,context):
        cur_obj = self.browse(cr,uid,ids,context)
        website_setting_obj = self.pool.get('website')
        sep = website_setting_obj.search(cr,uid,[])[0]
        site_data = website_setting_obj.browse(cr,uid,sep)
        template_sep = site_data.seo_product_separator
        title_str = ''
        if cur_obj.name:
            title_str += '{Name}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if cur_obj.category:
            title_str += '{Category}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if cur_obj.supplier:
            title_str += '{Supplier}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if cur_obj.description:
            title_str += '{Description}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if template_sep:
            if title_str.endswith(template_sep):
                cnt = len(title_str)
                title_str1 = title_str[:cnt-len(template_sep)]
        else:
            if title_str.endswith('-') :
                cnt = len(title_str)
                title_str1 = title_str[:cnt-1]
            else:
                title_str1 = title_str
        seoproducttemplate_obj = self.pool.get(context['active_model'])
        seoproducttemplate_obj.write(cr,uid,context['active_id'],{'title':title_str1})
        return True
    
class category_title_detail(osv.osv):
    
    _name = "seo.category.title.detail"
    
    _description = "SEO Category Title Details"
    
    _columns = {
                
            'name' : fields.boolean('Name'),
            'category' : fields.boolean('Category Name'),
    }
    
    def get_title_detail(self,cr,uid,ids,context):
        cur_obj = self.browse(cr,uid,ids,context)
        website_setting_obj = self.pool.get('website')
        sep = website_setting_obj.search(cr,uid,[])[0]
        site_data = website_setting_obj.browse(cr,uid,sep)
        template_sep =  site_data.seo_product_separator
        title_str = ''
        if cur_obj.name:
            title_str += '{Name}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if cur_obj.category:
            title_str += '{Category}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        
        if template_sep:
            if title_str.endswith(template_sep):
                cnt = len(title_str)
                title_str1 = title_str[:cnt-len(template_sep)]
        else:
            if title_str.endswith('-') :
                cnt = len(title_str)
                title_str1 = title_str[:cnt-1]
            else:
                title_str1 = title_str
        seoproducttemplate_obj = self.pool.get(context['active_model'])
        seoproducttemplate_obj.write(cr,uid,context['active_id'],{'title':title_str1})
        return True

class keyword_detail(osv.osv):
    
    _name = "seo.keyword.detail"
    
    _description = "SEO keyword Details"
    
    _columns = {
                
            'name' : fields.boolean('Name'),
            'supplier' : fields.boolean('Supplier Name'),
            'category' : fields.boolean('Category Name'),
            'description' : fields.boolean('Description For Quotation')
    }
    
    def get_keyword_detail(self,cr,uid,ids,context):
        cur_obj = self.browse(cr,uid,ids,context)
        website_setting_obj = self.pool.get('website')
        sep = website_setting_obj.search(cr,uid,[])[0]
        site_data = website_setting_obj.browse(cr,uid,sep)
        template_sep =  site_data.seo_product_separator
        title_str = ''
        if cur_obj.name:
            title_str += '{Name}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if cur_obj.category:
            title_str += '{Category}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if cur_obj.supplier:
            title_str += '{Supplier}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if cur_obj.description:
            title_str += '{Description}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        
        if template_sep:
            if title_str.endswith(template_sep):
                cnt = len(title_str)
                title_str1 = title_str[:cnt-len(template_sep)]
        else:
            if title_str.endswith('-') :
                cnt = len(title_str)
                title_str1 = title_str[:cnt-1]
            else:
                title_str1 = title_str
        seoproducttemplate_obj = self.pool.get(context['active_model'])
        seoproducttemplate_obj.write(cr,uid,context['active_id'],{'keyword':title_str1})
        return True

class category_keyword_detail(osv.osv):
    
    _name = "seo.category.keyword.detail"
    
    _description = "SEO Category keyword Details"
    
    _columns = {
                
            'name' : fields.boolean('Name'),
            'category' : fields.boolean('Category Name'),
    }
    
    def get_keyword_detail(self,cr,uid,ids,context):
        cur_obj = self.browse(cr,uid,ids,context)
        website_setting_obj = self.pool.get('website')
        sep = website_setting_obj.search(cr,uid,[])[0]
        site_data = website_setting_obj.browse(cr,uid,sep)
        template_sep =  site_data.seo_product_separator
        title_str = ''
        if cur_obj.name:
            title_str += '{Name}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if cur_obj.category:
            title_str += '{Category}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        
        if template_sep:
            if title_str.endswith(template_sep):
                cnt = len(title_str)
                title_str1 = title_str[:cnt-len(template_sep)]
        else:
            if title_str.endswith('-') :
                cnt = len(title_str)
                title_str1 = title_str[:cnt-1]
            else:
                title_str1 = title_str
        seoproducttemplate_obj = self.pool.get(context['active_model'])
        seoproducttemplate_obj.write(cr,uid,context['active_id'],{'keyword':title_str1})
        return True
class description_detail(osv.osv):
    
    _name = "seo.description.detail"
    
    _description = "SEO description Details"
    
    _columns = {
                
            'name' : fields.boolean('Name'),
            'supplier' : fields.boolean('Supplier Name'),
            'category' : fields.boolean('Category Name'),
            'description' : fields.boolean('Description For Quotation')
    }
    
    def get_description_detail(self,cr,uid,ids,context):
        cur_obj = self.browse(cr,uid,ids,context)
        website_setting_obj = self.pool.get('website')
        sep = website_setting_obj.search(cr,uid,[])[0]
        site_data = website_setting_obj.browse(cr,uid,sep)
        template_sep =  site_data.seo_product_separator
        title_str = ''
        if cur_obj.name:
            title_str += '{Name}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if cur_obj.category:
            title_str += '{Category}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if cur_obj.supplier:
            title_str += '{Supplier}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if cur_obj.description:
            title_str += '{Description}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        
        if template_sep:
            if title_str.endswith(template_sep):
                cnt = len(title_str)
                title_str1 = title_str[:cnt-len(template_sep)]
        else:
            if title_str.endswith('-') :
                cnt = len(title_str)
                title_str1 = title_str[:cnt-1]
            else:
                title_str1 = title_str
        seoproducttemplate_obj = self.pool.get(context['active_model'])
        seoproducttemplate_obj.write(cr,uid,context['active_id'],{'description':title_str1})
        return True
    
class category_description_detail(osv.osv):
    
    _name = "seo.category.description.detail"
    
    _description = "SEO Category description Details"
    
    _columns = {
                
            'name' : fields.boolean('Name'),
            'category' : fields.boolean('Category Name'),
    }
    
    def get_description_detail(self,cr,uid,ids,context):
        cur_obj = self.browse(cr,uid,ids,context)
        website_setting_obj = self.pool.get('website')
        sep = website_setting_obj.search(cr,uid,[])[0]
        site_data = website_setting_obj.browse(cr,uid,sep)
        template_sep =  site_data.seo_product_separator
        title_str = ''
        if cur_obj.name:
            title_str += '{Name}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        if cur_obj.category:
            title_str += '{Category}'
            if template_sep:
                title_str += template_sep
            else:
                title_str += '-'
        
        if template_sep:
            if title_str.endswith(template_sep):
                cnt = len(title_str)
                title_str1 = title_str[:cnt-len(template_sep)]
        else:
            if title_str.endswith('-') :
                cnt = len(title_str)
                title_str1 = title_str[:cnt-1]
            else:
                title_str1 = title_str
        seoproducttemplate_obj = self.pool.get(context['active_model'])
        seoproducttemplate_obj.write(cr,uid,context['active_id'],{'description':title_str1})
        return True
    
class success_update(osv.osv_memory):
    
    _name = "success.update"
    
    _description = "SEO Successful Update"
    
    _columns = {
                
            'name' : fields.char('Name',size=100,default="Congratulations ! All products SEO Information updated successfully."),
    }
class success_update_category(osv.osv_memory):
    
    _name = "success.update.category"
    
    _description = "SEO Successful Update Category"
    
    _columns = {
                
            'name' : fields.char('Name',size=100,default="Congratulations ! All Category SEO Information updated successfully."),
    }