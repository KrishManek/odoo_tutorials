
{
    'name': "Petrol Pum Management System",
    'summary': """App to manage Petrol Pump releated Services""",
    "description": """Petrol Pump Management System for Odoo 17 Community
        This module provides a comprehensive ERP solution for managing petrol pumps, including:
        
            - Station, tank, and dispenser hierarchy
            - Real-time fuel inventory tracking
            - Sale recording with automated stock deduction
            - Accounting integration with automatic invoice creation
            - Daily low stock alerts with email notifications
            - Dashboard views for daily sales and fuel status
            - Role-based access control for admins, station managers, and pump operators
            - Fuel price history tracking

        Designed for operational efficiency, transparency, and easy monitoring of fuel transactions and stock levels.""",
    "author": "Krish Manek",
    "version": "1.0",
    "depends": ['base', 'account','mail','base_setup', 'product','sale','stock','purchase', 'sale_management'],
    'sequence' : 1,
    'application' : True,
    'license' : 'LGPL-3',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/station_views.xml',
        'views/fuel_tank_views.xml',
        'views/dispenser_views.xml',
        'views/sale_line_views.xml',
        'views/petrol_pump_menus.xml',
        'wizards/replenish_tank_wizard.xml',
        'wizards/dispenser_dashboard_wizard.xml',
        'data/ir_cron.xml',
        'data/email_templates.xml',
        #'reports/report.xml',
        'reports/report_dispenser_dashboard.xml',
    ],
    'installable': True,
}
