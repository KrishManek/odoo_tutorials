from odoo import fields,models,api
from odoo.exceptions import ValidationError

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    special_pricelist = fields.Boolean(string="Special Pricelist")
    
    @api.constrains('special_pricelist', 'active')
    def _check_unique_special_pricelist(self):
        if self.special_pricelist and self.active:
            existing = self.search([
                ('id', '!=', self.id),
                ('special_pricelist', '=', True),
                ('active', '=', True)
            ], limit=1)
            if existing:
                raise ValidationError("Only one active Special Pricelist is allowed.")