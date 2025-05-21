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
        'wizard/assign_serial_view.xml',
        'wizard/manufacturing_report.xml',
        'wizard/update_produt_serial_view.xml',
        'wizard/update_produt_serial_view.xml',
        'views/product_product_views.xml',
        'views/mrp_production.xml',
        'views/sale_order_view.xml',
    ],
}