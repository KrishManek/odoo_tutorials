from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleRMAline(models.Model):
    _name = "sale.rma.line"
    _description = "Sale RMA Lines"
    

    rma_id = fields.Many2one('sale.rma', string="RMA Reference Id")
    product_id = fields.Many2one('product.product', string="Product")
    so_qty = fields.Float(string="SO Qty")
    unit_price = fields.Float(string="Unit Price")
    to_receive = fields.Float(string="To Receive")
    received_qty = fields.Float(string="Received Qty")
    returned_qty = fields.Float(string="Returned Qty")
    move_ids = fields.One2many("stock.move", 'rma_line_id', string="Sale RMA Line IDS")


