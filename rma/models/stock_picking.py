from odoo import fields,models,api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    rma_id = fields.Many2one('sale.rma', string="RMA ID")

    #lead_reference = fields.Char(string="Lead Reference", related='field_name')