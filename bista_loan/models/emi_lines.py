from odoo import models, fields, api


class EmiLines(models.Model):
    _name = 'emi.line'
    _rec_name = 'loan_id'
    
    loan_id = fields.Many2one('loan.management', string="Loan_id")
    paid_date = fields.Date(string="Paid date", default=fields.Date.today())
    interest_amount = fields.Float(string="Interest Amount.")
    principle_amount = fields.Float(string="Principle Amount.")
    total_paid = fields.Float(string="Amount Paid.")
    state = fields.Selection([('pending', 'Pending'),
                              ('invoiced', 'Invoice Created'),
                              ('paid', 'Invoice Paid'),], string="Status", default='pending')