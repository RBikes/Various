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
    'name' : 'Roetz Check Sale Shipped',
    'version' : '0.1',
    'author' : 'Roetz-Bikes BV',
    'summary': '',
    'description': """
Changes method of checking sale order delivery status.
Checks transfers instead of procurements. The shipped field is no longer
stored and cannot be searched. By necessity, this module redefines the
sale report without the shipped column.
    """,
    'category': 'Stock',
    'sequence': 6,
    'website' : 'www.roetz-bikes.com',
    'images' : [],
    'depends' : ['base','sale_stock'],
    'demo' : [],
    'data' : [
#        'view.xml',
    ],
    'test' : [
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
