from odoo import fields,models,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    orignal_price = fields.Float(string="Orignal Price", compute="_compute_previous_price", store=True)
    qty_in_move = fields.Float(string="Qty Available (Warehouse)", compute="_compute_available_quantity", store=True)
    qty_at_locations = fields.Float(string="Qty at Selected Locations", compute="_compute_available_quantity", store=True)
    location_ids = fields.Many2many('stock.location', string="Selected Locations")
    
    @api.depends('product_id', 'product_uom', 'product_uom_qty', 'order_partner_id.extra_discount')
    def _compute_discount(self):
        res = super(SaleOrderLine,self)._compute_discount()
        for order in self:
            order.discount += order.order_partner_id.extra_discount
        return res

    @api.depends('product_template_id','product_id.lst_price')
    def _compute_previous_price(self):
        for rec in self:
            rec.orignal_price = rec.product_id.lst_price

    """ @api.depends('order_id.warehouse_id')
    def _compute_available_warehouse_qty(self):
        for rec in self:
            qty = self.env['stock.quant'].search([('location_id','=',rec.order_id.warehouse_id),('product_id','=',rec.product_id)]).mapped('inventory_quantity_auto_apply')
            rec.qty_in_move = qty """
    
    @api.depends('order_id.warehouse_id', 'product_id', 'location_ids')
    def _compute_available_quantity(self):
        for line in self:
            product = line.product_id
            qty_wh = 0.0
            qty_locations = 0.0
            warehouse = line.order_id.warehouse_id

            if product and warehouse:   
                qty_wh = product.with_context(warehouse_id=warehouse.id).free_qty

            if product and line.location_ids:
                qty_locations = product.with_context(location=line.location_ids.ids).qty_available
            line.qty_in_move = qty_wh
            line.qty_at_locations = qty_locations