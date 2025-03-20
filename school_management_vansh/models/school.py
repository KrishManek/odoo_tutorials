from odoo import models, fields


class School(models.Model):
    _name = 'school.details'
    _description = 'School Details'
    _rec_name = 'school_name'

    school_name = fields.Char(string='School Name', required=True)
    address = fields.Text(string='Address')
    principal_name = fields.Char(string='Principal Name')
    contact_number = fields.Char(string='Contact Number')
    email = fields.Char(string='Email')

    student_ids = fields.One2many('student.details', 'school_name', string="Students")
    teacher_ids = fields.One2many('teacher.details', 'school_name', string="Teachers")
    book_ids = fields.One2many('books.details', 'school_name', string="Books")
    student_user_id = fields.Many2many('attendance.details', 'rel_student_user_id', column1='User_Id', column2='Student_User',string='Students')

    def action_open_school_wizard(self):
        view_id = self.env.ref('school_management.school_opening_wizard_wizard').id
        return {
            'name': 'School Feedback',
            'view_mode': 'form',
            'res_model': 'wizard.details',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }