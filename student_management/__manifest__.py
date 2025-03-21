# -*- coding: utf-8 -*-
{
    'name' : 'Student Management System',
    'author' : 'Krish',
    'description' : 'Student Management System',
    'depends' : ['base','product'],
    'sequence' : 1,
    'application' : True,
    'data' : [
        'security/ir.model.access.csv', 
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'views/student_view.xml', 
        'views/subject_view.xml', 
        'views/previous_year_marks.xml', 
        'views/tution_fee.xml', 
    ],
}