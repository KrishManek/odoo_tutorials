from odoo import fields, models

class Product(models.Model):
    _inherit = 'product.product'
    
    sequence_id = fields.Many2one('ir.sequence', string="Sequnence")