from odoo import models, fields, api

class Teacher(models.Model):
    _name = 'teacher.details'
    _description = 'Teacher'

    name = fields.Char(string="Teacher Name", required=True)
    contact = fields.Char(string="Contact")
    teacher_id = fields.Char(string="Teacher Id" ,readonly=True)
    salary = fields.Float(string="Salary")

    school_name = fields.Many2one('school.details', string='School Name')

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Teacher, self).create(vals_list)
        for record in res:
            record.teacher_id = self.env['ir.sequence'].next_by_code('teacher.details')
        return res

