# -*- coding: utf-8 -*-
{
    'name': 'Bista Crm Approval System',
    'desc': 'Bista SalCrmes Approval System',
    'author': 'Krish Manek',
    'depends': ['sale_crm','base_setup','crm'],
    'sequence': 1,
    'application': 'true',
    'version': '1.0',
    'data': [
        'security/ir.model.access.csv',
        'data/stage_data.xml',
        'views/crm_lead_view.xml',
        'views/probability_stage_view.xml',
        'views/sale_order_view.xml'
    ],
}