#########################################################################
# Copyright (C) 2009  Sharoon Thomas, Open Labs Business solutions      #
#                                                                       #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
#(at your option) any later version.                                    #
#                                                                       #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                       #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#########################################################################
from openerp.osv import osv, fields
import base64
import urllib
from openerp import tools


class product_images(osv.Model):

    "Products Image gallery"
    _name = "product.images"
    _description = __doc__
    _table = "product_images"

    def get_image_link(self, cr, uid, id):
        each = self.read(cr, uid, id, ['link', 'filename', 'image'])
        if each['link']:
            try:
                (filename, header) = urllib.urlretrieve(each['filename'])
                f = open(filename, 'rb')
                img = base64.encodestring(f.read())
                f.close()
            except:
                img = ''
        else:
            img = each['image']
        return img

    def get_image_custom(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for each in ids:
            obj = self.browse(cr,uid,ids,context=context)
            if obj.link:
                res[each] = self.get_image_link(cr, uid, each)
            else:
                res[each] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return res

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

    #def _get_image(self, cr, uid, ids, name, args, context=None):
    #    result = dict.fromkeys(ids, False)
    #    for obj in self.browse(cr, uid, ids, context=context):
    #        result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
    #    return result

    _columns = {
        'name': fields.char('Image Title', size=100, required=True),
        'link': fields.boolean('Link?',
                               help="""Images can be linked from files on your
                                       file system or remote (Preferred)"""),
        'image': fields.binary('Image'),
        'filename': fields.char('File Location', size=250),
        #'preview': fields.function(get_image_custom, type="binary", method=True),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image", 
            store={
                'product.images': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            }),
        #'image_small': fields.function(get_image_custom, type="binary", method=True),
        'comments': fields.text('Comments'),
        'product_id': fields.many2one('product.template', 'Product'),
    }

    _defaults = {
        'link': lambda *a: True,
    }
