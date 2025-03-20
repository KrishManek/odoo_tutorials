# -*- coding: utf-8 -*-
{
    'name': 'Hospital Management',
    'description': 'Hospital Management System',
    'author': 'Krish',
    'depends': ['base','product'],
    'sequence': 1,
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/hospital_view.xml',
        'views/specialization_view.xml',
        'views/prescription_view.xml',
        'views/prescription_line_view.xml',
        'views/appointments_view.xml',
    ],
}
