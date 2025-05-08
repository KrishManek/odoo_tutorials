# -*- coding: utf-8 -*-
{
    'name': 'Sale RMA',
    'desc': 'Sale RMA',
    'author': 'Krish Manek',
    'depends': ['base', 'product', 'sale', 'sale_stock', 'account'],
    'sequence': 1,
    'application': True,
    'version': '1.0',
    'data': [
        'security/ir.model.access.csv',
        'views/sale_rma_views.xml',
        'views/rma_team_views.xml',
        'views/sale_order_view.xml',
        'wizard/rma_wizard_view.xml',
        'wizard/rma_invoice_view.xml',
        
    ],
}