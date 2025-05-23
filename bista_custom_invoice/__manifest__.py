# -*- coding: utf-8 -*-
{
    'name': 'Bista Custom Invoice',
    'desc': 'Custom Invoice',
    'author': 'Krish Manek',
    'depends': ['base','account'],
    'sequence': 1,
    'application': 'true',
    'version': '1.0',
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_view.xml',
    ],
}