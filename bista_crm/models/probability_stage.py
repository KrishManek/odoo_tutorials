from odoo import fields, models,api
from odoo.exceptions import ValidationError

class CRMProbabilityStage(models.Model):
    _name = 'probability.stage'
    _description = 'Probability Stage'
    
    name = fields.Char(string="Stage")
    percentage = fields.Float(string="Precentage %")
    
    @api.constrains('percentage')
    def _check_percentage(self):
        for record in self:
            if record.percentage >= 100 and record.percentage <= 0:
                raise ValidationError("Please enter percentage value between 0 - 100 only")
    