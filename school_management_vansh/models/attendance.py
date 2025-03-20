from odoo import models, fields

class Attendance(models.Model):
    _name = 'attendance.details'
    _description = 'Attendance'
    _rec_name = 'student_name'

    student_name = fields.Char(string="Student Name", required=True)
    date = fields.Date(string="Date", required=True)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
    ], string='Status', required=True)

    school_name = fields.Many2one('school.details', string='School Name')
    res_user_ids = fields.Many2many('res.users','rel_user_id',column1='User_Id',column2='User',string='Users')
    student_users_ids = fields.Many2many('student.details','rel_student_id',column1='User_Id',column2='Student_User',string='Students')