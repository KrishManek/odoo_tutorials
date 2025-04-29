from odoo import models, fields,api
from odoo.exceptions import ValidationError

class RMAWizard(models.TransientModel):
    _name = 'sale.wizard'
    _description = 'Sale Add Product Wizard'

    sale_id = fields.Many2one('sale.order',string="Default_id")
    product_ids = fields.Many2many('product.product', string="Products")
    
    def add_products(self):
        product_lines = []
        for product in self.product_ids:
            product_lines.append((0, 0, {
                        'product_id': product.id,
                        'product_uom_qty': 1,
                    }))
        self.sale_id.order_line = product_lines
            