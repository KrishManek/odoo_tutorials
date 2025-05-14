from odoo import fields,models,api

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    loan_id = fields.Many2one('loan.management', string="Loan Id.")
    
    