from odoo import fields, models,api
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    remaining_balance = fields.Float(string="Remaining Balance", compute="_compute_remaining_amount", store=True)
    customer_invoices = fields.One2many('invoice.move', 'payment_id')
    
    def action_post(self):
        res = super().action_post()
        line_id = self.move_id.line_ids.filtered(lambda line: line.account_type == 'asset_receivable').id
        for invoice in self.customer_invoices:
            #print(self)
            self.move_id.line_ids.write({'is_custom_paid_invoice': True})
            #line_id = self.env['account.move.line'].search([('move_type', '=', 'entry'), ('move_id', '=', self.move_id.id), ('account_type', '=', 'asset_receivable')]).id
            result = invoice.invoice_id.js_assign_outstanding_line(line_id)
            #print(invoice)
        return res
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.customer_invoices = [(5, 0, 0)]
            invoice_data = self.env['account.move'].search([('partner_id', '=', self.partner_id.id),('move_type', '=', 'out_invoice'), ('amount_residual', '>=', 1), ('state', '=', 'posted')]) 
            data = []
            amount = 0
            for invoice in invoice_data:
                if invoice.amount_residual > 0:
                    data.append((0, 0, {
                        'payment_id' : self.id,
                        'invoice_id': invoice.id,
                        'invoice_date' : invoice.invoice_date,
                        'amount_residual' : invoice.amount_residual,
                    }))
                    amount += invoice.amount_residual
            self.customer_invoices = data
            self.amount = amount
            
    @api.depends('amount', 'customer_invoices.allocation_amount')
    def _compute_remaining_amount(self):
        for invoice in self:
            allocated_amt = 0
            for line in invoice.customer_invoices:
                if line.allocation_amount < 0:
                    line.allocation_amount = 0
                    #raise ValidationError("Amount can't be negative") 
                if line.allocation_amount >  line.amount_residual:
                    if (invoice.amount - allocated_amt) > line.amount_residual:  
                        line.allocation_amount = line.amount_residual
                    else:
                        line.allocation_amount = invoice.amount - allocated_amt 
                    #raise ValidationError(f"Allocation Amount must be less than Invoice Amount i.e {line.amount_residual}")
                allocated_amt += line.allocation_amount
                if invoice.amount >= allocated_amt:
                    invoice.remaining_balance = invoice.amount - allocated_amt
                else:
                    invoice.remaining_balance = 0
                #raise UserError("No Amount left for allocation.")
    
        
    """ @api.depends('amount', 'customer_invoices.allocation_amount')
    def _compute_remaining_amount(self):
        for invoice in self:
            allocated_amt = sum(invoice.customer_invoices.mapped('allocation_amount'))
            if invoice.amount >= allocated_amt:
                invoice.remaining_balance = invoice.amount - allocated_amt
            else:
                invoice.remaining_balance = 0
                #raise UserError("No Amount left for allocation.")
     """
    @api.onchange('amount')
    def _onchange_amount(self):
        amount = self.amount
        for invoice in self.customer_invoices:    
            if invoice.amount_residual > amount and amount > 0:
                invoice.allocation_amount = amount
                amount-= amount
            elif invoice.amount_residual < amount and amount > 0:
                invoice.allocation_amount = invoice.amount_residual
                amount -= invoice.amount_residual 
            else:
                invoice.allocation_amount = 0
             
    """  @api.depends('amount', 'customer_invoices.allocation_amount')
    def _compute_allocated_amount(self):
        for invoice in self:
            invoice.remaining_balance = invoice.amount - sum(invoice.customer_invoices.mapped('allocation_amount'))
              """

              
