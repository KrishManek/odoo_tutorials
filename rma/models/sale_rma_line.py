from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleRMAline(models.Model):
    _name = "sale.rma.line"
    _description = "Sale RMA Lines"
    

    rma_id = fields.Many2one('sale.rma', string="RMA Reference Id")
    product_id = fields.Many2one('product.product', string="Product")
    so_qty = fields.Float(string="SO Qty")
    unit_price = fields.Float(string="Unit Price")
    to_receive = fields.Float(string="To Receive", compute='_compute_delivered_qty', store=True)
    move_ids = fields.One2many("stock.move", 'rma_line_id', string="Sale RMA Line IDS")
    received_qty = fields.Integer(string="Delivered Quantity", compute='_compute_delivered_qty', store=True)
    remaining_qty = fields.Integer(string="Remaining  Quantity" ,compute="_compute_remaining_qty", store=True)

    
    #@api.depends('move_ids','move_ids.state')
    def _compute_delivered_qty(self):
        for rec in self:
           rec.received_qty = sum(rec.move_ids.filtered(lambda m: m.state == 'done').mapped('quantity'))
           
    #@api.depends('move_ids','move_ids.state')
    def _compute_remaining_qty(self):
        for rec in self:
            rec.to_receive = sum(rec.move_ids.mapped('product_uom_qty'))
            rec.remaining_qty = rec.to_receive - rec.received_qty

