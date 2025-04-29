# -*- coding: utf-8 -*-
{
    'name': 'Bista Exam 2',
    'desc': 'Bista Exam 2',
    'author': 'Krish Manek',
    'depends': ['sale','base_setup','purchase'],
    'sequence': 1,
    'application': 'true',
    'version': '1.0',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/pharmacy_view.xml',
        'views/product_view.xml',
        'views/invoice_view_inherit.xml',
        'views/sales_order_views.xml',
        'views/mail_activity_view.xml',
        'data/pharma_data.xml',
        'report/stock_report_deliveryslip.xml',
        'wizard/sale_wizard_view.xml',
        'views/res_config_setings_view.xml',
    ],
}