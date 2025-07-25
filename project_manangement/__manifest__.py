{
    'name': 'Tms Optimizeit Project Management',
    'version': '1.0.0',
    'summary': 'TMS Optimizeit Project Management Module',
    'description': """
This module is designed to enhance the project management capabilities of the TMS Optimizeit system. It integrates various features such as advanced filtering, dynamic list views, and enhanced web functionalities to streamline project management processes.
    """,
    'author': 'Krish',
    'website': '',
    'depends': [
        'base',
        'project',
        'web',
        'project_todo',
        'hr_timesheet',
    ],
    'data': [
        'views/project_task_views.xml',

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
