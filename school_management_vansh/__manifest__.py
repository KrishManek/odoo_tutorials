# -*- coding: utf-8 -*-
{
    'name': 'School Management',
    'description': 'Manage Schools',
    'author': 'Krish',
    'depends': ['base'],
    'sequence': 1,
    'application': True,

    'data': [
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
        'views/school_view.xml',
        'views/fees_view.xml',
        'views/student_view.xml',
        'views/teacher_view.xml',
        'views/attendance_view.xml',
        'views/books_view.xml',
        'wizard/school_information_wizard.xml',

    ],
}

