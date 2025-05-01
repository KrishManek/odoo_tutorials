# -*- coding: utf-8 -*-
{
    'name': 'Bista Manufacturing',
    'desc': 'Bista Manufacturing',
    'author': 'Krish Manek',
    'depends': ['sale','purchase','mrp','stock'],
    'sequence': 1,
    'application': 'true',
    'version': '1.0',
    'data': [
        'security/ir.model.access.csv',
        'views/product_product_views.xml',
        'views/mrp_production.xml',
        'wizard/assign_serial_view.xml',
        'views/sale_order_view.xml',
    ],
}