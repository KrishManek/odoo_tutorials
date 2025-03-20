{
    'name' : 'Gym Management',
    'author' : 'Krish',
    'description' : 'Gym Management System',
    'depends' : ['base'],
    'sequence' : 1,
    'application' : True,


    'data' : [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'views/members_view.xml',
        'views/plans_view.xml',
        'views/log_in_view.xml',
        'views/trainers_view.xml',
    ],


}