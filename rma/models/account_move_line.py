from odoo import fields,models,api

class StockPicking(models.Model):
    _inherit = 'account.move.line'

    rma_line_id = fields.Many2one('sale.rma.line', string="Sale line RMA")