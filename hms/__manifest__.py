# -*- coding: utf-8 -*-
{
    'name':'Hospital Management System',
    'desc':'Hospital Management',
    'author':'Krish Manek',
    'depends':['base','product'],
    'sequence':1,
    'application':'true',
    'version':'1.0',
    'data':[
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'views/patient_view.xml',
        'views/appointment_view.xml',
        'views/doctor_view.xml',
        'views/hospital_view.xml',
        'views/specialization.xml',
    ],
}

