from odoo import fields,models
class TeacherDetails(models.Model):
    _name = "teacher.details"
    _description = "teacher_Details"

    name = fields.Char(String="Name")
    id = fields.Integer(String="Roll No")       
    school_id = fields.Many2one('school.details', string="School")
    teaches_in = fields.One2many('standard.details', 'std_id', string="Teaches in")  
    student_ids = fields.One2many('student.details', 'teacher_id', string="Students")
    