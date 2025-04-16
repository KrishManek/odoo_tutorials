from odoo import fields, models, api
from odoo.exceptions import ValidationError


class RMAInvoiceLine(models.TransientModel):
    _name = 'rma.invoice.wizard.line'
    _description = 'RMA Invoice Wizard Lines'
    
    rma_invoice_wizard_id = fields.Many2one('rma.invoice.wizard', string="Wizard id.")
    product_id = fields.Many2one('product.product', string="Product")
    so_qty = fields.Float(string="SO Qty")
    #return_qty = fields.Float(string="Qty to invoice")
    rma_line_id = fields.Many2one('sale.rma.line', string="sale Rma Line Id.")
    to_invoiced = fields.Float(string="Qty to invoice")

