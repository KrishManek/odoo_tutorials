from odoo import fields,models,api
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def button_validate(self):
        result = super().button_validate()
        self.message_post(body=f"Record is validated by {self.env.user.name}.")
        return result
    
    