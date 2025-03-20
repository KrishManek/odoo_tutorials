# -*- coding: utf-8 -*-
{
    'name': 'Hospital Management System',  # Module name
    'desc': 'Hospital Management',  # Module description
    'author': 'Krish Manek',  # Author name
    'depends': ['base', 'product'],  # Dependencies
    'sequence': 1,  # Sequence in which the module should be loaded
    'application': 'true',  # Whether the module is an application
    'version': '1.0',  # Module version
    'data': [
        'security/ir.model.access.csv',  # Access control list
        'data/ir_sequence.xml',  # Sequence data
        'data/ir_cron.xml',  # Cron job data
        'views/patient_view.xml',  # Patient view
        'views/appointment_view.xml',  # Appointment view
        'views/doctor_view.xml',  # Doctor view
        'views/hospital_view.xml',  # Hospital view
        'views/specialization.xml',  # Specialization view
        'views/prescription_view.xml',  # Prescription view
        'views/prescription_line_view.xml',  # Prescription line view
    ],
}