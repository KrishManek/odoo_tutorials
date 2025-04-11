from odoo import fields,models,api

class StockPicking(models.Model):
    _inherit = 'stock.move'

    rma_line_id = fields.Many2one('sale.rma.line', string="Sale RMA Lines")

    #lead_reference = fields.Char(string="Lead Reference", related='field_name')