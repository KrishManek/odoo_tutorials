from odoo import models, fields, api


class InterestRate(models.Model):
    _name = 'interest.rate'
    _rec_name = 'rate'
    
    loan_id = fields.Many2one('loan.management', string="Loan_id")
    rate = fields.Float(string="Interest Rate", default=1)
    starting_date = fields.Date(string="Date.", default = fields.Date.today())
    is_active = fields.Boolean(string="Active")
    
    def active_rate(self):
        if self.rate and self.starting_date:
            active_recs = self.env['interest.rate'].search([('is_active', '=', True), ('loan_id', '=', self.loan_id.id)])
            active_recs.write({'is_active' : False})
            self.is_active = True        
            self.loan_id.rate_of_interest = self.rate