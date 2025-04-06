from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    lead_reference = fields.Char(string="Lead Reference")
    
