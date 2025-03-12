from odoo import fields,models
class StudentsDetails(models.Model):
    _name = "student.details"
    _description = "Student_Details"

    name = fields.Char(String="Name")
    roll_no = fields.Integer(String="Roll No.")
    school_id = fields.Many2one('school.details', string="School")
    teacher_id = fields.Many2one('teacher.details', string="Teacher")
    school_ids = fields.Many2many('school.details','rel_school_student', 'school', 'student', string= "Students") 
