from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    prescription_line_id = fields.Many2one("prescription.line",
                                           string="Prescription Line",  ondelete="cascade")