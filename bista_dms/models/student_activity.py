from odoo import fields, models

class StudentActivity(models.Model):
    _name = 'student.activity'
    _description = 'Student Activity'
    
    name = fields.Char(string="Name")