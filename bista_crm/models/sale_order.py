from odoo import fields,models,api
from odoo.exceptions import UserError
class SaleOrder(models.Model):
    _inherit = 'sale.order'


    probability_stage = fields.Many2one('probability.stage', related='opportunity_id.probability_stage', store=True, string="Probability Stage")
    
    def action_confirm(self):
        if not self.probability_stage:
            stage = self.env['probability.stage'].search([('percentage','=','100.00')])
            if stage:
                self.probability_stage = stage.id
            else:
                raise UserError("Please Create a stage for 100% and then try to confirm the order")
        res = super(SaleOrder, self).action_confirm()
        return res
