from odoo import fields, models

class SchoolDetails(models.Model):
    _name = "school.details"
    _description = "School_Details"

    name = fields.Char(String="name")
    desc = fields.Text(String="Description")
    student_ids = fields.One2many('student.details', 'school_id', String="Student")
    teacher_ids = fields.One2many('teacher.details', 'school_id', String="Teacher")
    school_user_ids = fields.Many2many("res.users",'rel_school_user','user_id','school_user_ids', string="Users")
    school_user_teacher_ids = fields.Many2many("res.users",'rel_school_user','user_id','school_user_ids', string="Users")
    school_student_ids = fields.Many2many("student.details", "rel_student_school", "student", "school",string="Students")

    def action_open_wizard(self):
        veiw_id = self.env.ref("school_management.school_opening_wizard_wizard").id
        return {
            'name' : "Opening Date",
            'view_mode' : "form",
            'res_model' : 'school.opening.wizard',
            'view_id' : veiw_id,
            'type' : "ir.actions.act_window",
            'target' : 'new',
        }
        