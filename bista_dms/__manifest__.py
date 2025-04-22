# -*- coding: utf-8 -*-
{
    'name': 'Bista Document Management System',
    'desc': 'Bista Document Management System',
    'author': 'Krish Manek',
    'depends': ['base','sale','product'],
    'sequence': 1,
    'application': 'true',
    'version': '1.0',
    'data': [
        'security/ir.model.access.csv',
        'views/documents_custom_view.xml',
        'views/doc_tag_master_view.xml',
        'views/res_partner_view.xml',
        'views/product_product_view.xml',
        'views/sale_order_view.xml',
        'views/stock_picking.xml',
        'report/stock_report_deliveryslip.xml',
    ],
}