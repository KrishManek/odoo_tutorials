from odoo import fields, models,api
from odoo.exceptions import ValidationError

class InvoiceMove(models.Model):
    _name = 'invoice.move'
    
    payment_id = fields.Many2one('account.payment', string="Payment_id")
    invoice_id = fields.Many2one('account.move', string="Invoice_id")
    invoice_date = fields.Date(string="Invoice Date")
    amount_residual = fields.Float(string="Remaining Amount")
    allocation_amount = fields.Float(string="Allocated Amount")
    
            
    @api.constrains('allocation_amount')
    def _validate_allocation_amount(self):
        for invoice in self:
            if invoice.allocation_amount < 0:
                raise ValidationError("Amount cannot be Negative")      
            if invoice.allocation_amount > invoice.amount_residual:                    
                raise ValidationError(f"Allocation Amount must be less than Invoice Amount i.e {invoice.amount_residual}")