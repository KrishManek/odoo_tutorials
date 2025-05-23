# -*- coding: utf-8 -*-
{
    'name': 'Hospital Management System',  # Module name
    'desc': 'Hospital Management',  # Module description
    'author': 'Krish Manek',  # Author name
    'depends': ['base', 'product', 'sale', 'sale_stock', 'account'],  # Dependencies
    'sequence': 1,  # Sequence in which the module should be loaded
    'application': 'true',  # Whether the module is an application
    'version': '1.0',  # Module version
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',  # Access control list
        'data/ir_sequence.xml',  # Sequence data
        'data/ir_cron.xml',  # Cron job data
        'data/mail_template.xml',
        'views/patient_view.xml',  # Patient view
        'views/appointment_view.xml',  # Appointment view
        'views/doctor_view.xml',  # Doctor view
        'views/hospital_view.xml',  # Hospital view
        'views/specialization.xml',  # Specialization view
        'views/prescription_view.xml',  # Prescription view
        'views/prescription_line_view.xml',  # Prescription line view
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/report.xml',
        'views/prescription_report_view.xml',
        'views/product.xml',
        'wizard/update_qty_wizard_view.xml',
        'views/custom_sale_template.xml',
        'views/purchase_order_view.xml',
    ],
}
#'views/sale_order_view.xml',