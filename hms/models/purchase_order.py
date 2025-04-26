from odoo import fields,models,api
from odoo.exceptions import UserError

class Purchase(models.Model):
    _inherit = 'purchase.order'
    
    category_id = fields.Many2one('product.category', string="Category")
     