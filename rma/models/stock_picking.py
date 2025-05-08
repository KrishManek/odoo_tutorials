from odoo import fields,models,api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    rma_id = fields.Many2one('sale.rma', string="RMA ID")
    
    @api.depends('picking_type_id', 'partner_id','sale_id.order_line.location_id')
    def _compute_location_id(self):
        super()._compute_location_id()
        for picking in self:
            if self.sale_id.order_line.location_id:
                for line in picking.sale_id.order_line:
                    if picking.sale_id.order_line.location_id and (line.product_id in picking.move_ids.product_id):
                        picking.location_id = line.location_id
    #lead_reference = fields.Char(string="Lead Reference", related='field_name')