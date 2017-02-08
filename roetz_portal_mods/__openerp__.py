# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Ecosoft Co., Ltd. (http://ecosoft.co.th).
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

{
    'name' : 'Roetz Portal Modifications',
    'version' : '0.1',
    'author' : 'Roetz-Bikes BV',
    'summary': 'Modifies Portal Menus',
    'description': """


    """,
    'category': 'Technical',
    'sequence': 6,
    'website' : 'www.roetz-bikes.com',
    'images' : [],
    'depends' : ['base','portal','portal_sale'],
    'demo' : [],
    'data' : [
        'views.xml',
    ],
    'css': [],
    'test' : [
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
