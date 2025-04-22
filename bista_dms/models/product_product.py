from odoo import fields,models,api
from odoo.exceptions import UserError

class Product(models.Model):
    _inherit = 'product.product'
    
    document_ids = fields.Many2many('documents.custom', string="Documents")
     