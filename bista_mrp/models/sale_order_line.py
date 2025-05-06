from odoo import fields,models,api
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    process_qty = fields.Float(string="Process Quantity")
    
    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        self.process_qty = self.product_uom_qty

    # @api.constrains('process_qty')
    # def _validate_process_qty(self):
    #     if self.process_qty > self.product_uom_qty:
    #         raise UserError(f"Pricess Quantity must be less than Sale Quantity i.e. {self.product_uom_qty}")