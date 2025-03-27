{
    'name': "Bista HMS",
    'summary': """App to manage hospital""",
    "description": """this app will help to manage hospital""",
    "author": "Bista Solutions Pvt.Ltd",
    "version": "18.0",
    "depends": ['base', 'product'],
    "data": [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'views/res_patient_view.xml',
        'views/appointment_view.xml',
        'views/prescription_view.xml',
    ],
}