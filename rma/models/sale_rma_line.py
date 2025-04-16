from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleRMAline(models.Model):
    _name = "sale.rma.line"
    _description = "Sale RMA Lines"
    

    rma_id = fields.Many2one('sale.rma', string="RMA Reference Id")
    product_id = fields.Many2one('product.product', string="Product")
    so_qty = fields.Float(string="SO Qty")
    unit_price = fields.Float(string="Unit Price")
    to_receive = fields.Float(string="To Receive", compute='_compute_qty', store=True)
    move_ids = fields.One2many("stock.move", 'rma_line_id', string="Sale RMA Line IDS")
    received_qty = fields.Integer(string="Delivered Quantity", compute='_compute_qty', store=True)
    remaining_qty = fields.Integer(string="Remaining  Quantity" ,compute="_compute_qty", store=True)
    invoice_line_ids = fields.One2many("account.move.line", 'rma_line_id', string="Sale RMA Line IDS")
    invoiced_qty = fields.Float(string="Invoiced Qty",compute = "_compute_invoice_qty", store=True)
    qty_to_invoice = fields.Float(string="Quantitiy to Invoice", compute = "_compute_invoice_qty", store=True)

    
    @api.depends('move_ids.state','move_ids.product_uom_qty','move_ids.quantity')
    def _compute_qty(self):
        for rec in self:
            rec.received_qty = sum(rec.move_ids.filtered(lambda m: m.state == 'done').mapped('quantity'))
            rec.to_receive = sum(rec.move_ids.mapped('product_uom_qty'))
            rec.remaining_qty = rec.to_receive - rec.received_qty

    @api.depends('invoice_line_ids.move_id.state','invoice_line_ids.quantity','to_receive')
    def _compute_invoice_qty(self):
        for rec in self:
            rec.invoiced_qty = sum(rec.invoice_line_ids.filtered(lambda m: m.move_id.state != 'cancel').mapped('quantity'))
            rec.qty_to_invoice = rec.to_receive - rec.invoiced_qty

