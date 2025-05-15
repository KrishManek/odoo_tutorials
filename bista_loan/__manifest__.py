{
    'name': "Bista Loan Management System",
    'summary': """App to manage Loan Services""",
    "description": """this app will help to manage Loans""",
    "author": "Krish Manek",
    "version": "18.0",
    "depends": ['base', 'account'],
    'sequence' : 1,
    'application' : True,


    "data": [
        #'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/emi_product.xml',
        'data/email_template.xml',
        'views/loan_management_view.xml',
        'views/account_view.xml',
        'wizards/view_account_payment_register.xml',
    ],
}