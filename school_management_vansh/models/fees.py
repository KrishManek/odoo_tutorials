from odoo import fields,models,api


class Fees(models.Model):
    _name = 'fees.details'
    _description = 'Fees Information'

    student_id = fields.Many2one('student.details', string="Student")
    due_date = fields.Date(string="Due Date")
    amount_due = fields.Float(string="Amount Due")
    paid = fields.Boolean(string="Paid", default=False)

    def _Fees_Reminder(self):
        students = self.env['fees.details'].search([('due_date', '<=', fields.date.today()),('paid', '=', False)])
        for reminder in students:
            message = f"Reminder : Student {reminder.student_id.name} has a due fees of ₹{reminder.amount_due}"
            print(message)


