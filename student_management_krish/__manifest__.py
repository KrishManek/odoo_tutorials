# -*- coding: utf-8 -*-

{
    'name' : 'Student Management',
    'summary': """App for Student Management for Final Evaluation at Bista Baroda for Krish """,
    'author' : 'Krish',
    'description' : 'App for Student Management for Final Evaluation at Bista Solutions Baroda branch for Krish',
    "version": "18.0",
    'depends' : ['base', 'purchase', 'sale_management', 'account', 'mail', 'sale_stock'],
    'sequence' : 1,
    'application' : True,
    'license' : 'LGPL-3',
    'data' : [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/project_estimation_view.xml',
        'views/purchase_order_line_view.xml',
        'wizard/sales_excel_report.xml',
        'views/menu.xml',
        
    ],
}