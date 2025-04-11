from odoo import fields, models, api
from odoo.exceptions import ValidationError


class RMAWizardLine(models.TransientModel):
    _name = 'rma.wizard.line'
    _description = 'RMA Processing Wizard Lines'
    
    rma_wizard_id = fields.Many2one('rma.wizard', string="Wizard id.")
    product_id = fields.Many2one('product.product', string="Product")
    so_qty = fields.Float(string="SO Qty")
    return_qty = fields.Float(string="Qty to Return ")


    """  @api.constrains('return_qty')
    def validate_qty(self):
        for rec in self:
            if rec.so_qty < rec.return_qty:
                raise ValidationError(f"Return Quantity must be less than sale Qty i.e. {rec.so_qty}") """