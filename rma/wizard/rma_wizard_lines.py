from odoo import fields, models, api
from odoo.exceptions import ValidationError


class RMAWizardLine(models.TransientModel):
    _name = 'rma.wizard.line'
    _description = 'RMA Processing Wizard Lines'
    
    rma_wizard_id = fields.Many2one('rma.wizard', string="Wizard id.")
    product_id = fields.Many2one('product.product', string="Product")
    so_qty = fields.Float(string="SO Qty")
    return_qty = fields.Float(string="Qty to Return ")
    rma_line_id = fields.Many2one('sale.rma.line', string="sale Rma Line Id.", store=True, force_save=True)
"""     to_invoiced = fields.Float(string="Qty to invoice", compute="_compute_inv_qty", store=True)
    
    @api.depends('invoice_line_ids.quantity','rma_line_id.to_receive')
    def _compute_inv_qty(self):
        for rec in self:
            rec.to_invoiced = rec.rma_line_id.qty_to_invoice
 """
