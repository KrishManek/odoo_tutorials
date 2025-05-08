from odoo import fields, models, api

class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    child_warehouse_id = fields.Many2one('stock.location', string='Child Warehouse')
    