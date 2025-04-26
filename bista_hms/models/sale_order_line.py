from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    extra_note = fields.Text(string="Extra Note")
    location_ids = fields.Many2many("stock.location", string="Locations")
    quantity_available_at_locations = fields.Float(string="Available Quantity",
                                                   compute="_compute_quantity_available_at_locations")
    quantity_available_at_wh = fields.Float(string="Available Quantity at Warehouse",
                                                   compute="_compute_quantity_available_at_locations")

    def _compute_quantity_available_at_locations(self):
        for rec in self:
            rec.quantity_available_at_locations = rec.product_id.with_context(location=rec.location_ids.ids).qty_available
            rec.quantity_available_at_wh = rec.product_id.with_context({warehouse_id: rec.order_id.warehouse_id.id}).qty_available