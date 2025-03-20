from odoo import models, fields, api


class Student(models.Model):
    _name = 'student.details'
    _description = 'Student Details'

    student_id = fields.Char(string="Student ID")
    name = fields.Char(string='Student Name', required=True)
    enroll_no = fields.Char(string='Enrollment No', required=True)
    age = fields.Integer(string='Age')
    dob = fields.Date(string='Date of Birth')
    contact_no = fields.Char(string='Contact Number')

    school_name = fields.Many2one('school.details', string='School Name', required=True)

    @api.model_create_multi
    def create(self,vals_list):
        res = super(Student,self).create(vals_list)
        for record in res:
            record.student_id = self.env['ir.sequence'].next_by_code('student.details')
        return res
