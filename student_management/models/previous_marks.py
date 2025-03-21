from odoo import fields, models, api


class PreviousYearMarks(models.Model):
    _name = "previous.years.marks"
    _description = "Previous Years Marks"
    _res_name = 'student_id'

    student_id = fields.Many2one('res.student',string="Student")
    subject_id =  fields.Many2one('subject.subject',string="Subject", required=True)
    total_marks = fields.Float(string="Total Marks", required=True)
    obtained_marks_exam = fields.Float(string="Marks Obtained in Exam", required=True)
    obtained_marks_viva = fields.Float(string="Marks Obtained in Viva", required=True)
    total_obtained = fields.Float(string="Total Obtained Marks", compute='_compute_marks', store=True)

    @api.depends('obtained_marks_exam','obtained_marks_viva')
    def _compute_marks(self):
        for record in self:
            self.total_obtained = record.obtained_marks_exam + record.obtained_marks_viva
