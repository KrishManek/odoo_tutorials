from odoo import fields,models,api

class StockPicking(models.Model):
    _inherit = 'stock.move'

    prescription_line_id = fields.Many2one('hms.prescription.line', string="Prescription Lines")

    #lead_reference = fields.Char(string="Lead Reference", related='field_name')