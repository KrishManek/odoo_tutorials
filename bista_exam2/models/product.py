from odoo import fields,models,api
from odoo.exceptions import UserError

class Product(models.Model):
    _inherit = 'product.template'
    
    pharmacy_id = fields.Many2one('bista.pharma', string="Pharmacy")
    
    