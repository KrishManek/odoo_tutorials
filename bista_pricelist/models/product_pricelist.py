from odoo import fields,models,api
from odoo.exceptions import ValidationError

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    special_pricelist = fields.Boolean(string="Special Pricelist")
    
    """ @api.onchange('special_pricelist')
    def _onchange_special_pricelist(self):
        if self.special_pricelist:
            existing = self.search([
                ('id', '!=', self.id),
                ('special_pricelist', '=', True),
                ('active', '=', True)
            ], limit=1)
            if existing:
                existing.special_pricelist = False
                self.special_pricelist = True """
    
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