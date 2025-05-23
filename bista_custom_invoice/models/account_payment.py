from odoo import fields, models,api
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    remaining_balance = fields.Float(string="Remaining Balance", compute="_compute_remaining_amount", store=True)
    customer_invoices = fields.One2many('invoice.move', 'payment_id')
    
    def action_post(self):
        res = super().action_post()
        invoices = self.customer_invoices.mapped('invoice_id')
        for invoice in self.customer_invoices:
            print(self)
            self.move_id.line_ids.write({'is_custom_paid_invoice': True})
            line_id = self.move_id.line_ids.filtered(lambda line: line.account_type == 'asset_receivable').id
            #line_id = self.env['account.move.line'].search([('move_type', '=', 'entry'), ('move_id', '=', self.move_id.id), ('account_type', '=', 'asset_receivable')]).id
            result = invoice.invoice_id.js_assign_outstanding_line(line_id)
            print(invoice)
            
            #break 
            
    
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

class AccountMove(models.Model):
    
    _inherit = 'account.move'
    
    @api.model_create_multi
    def create(self, vals_list):
        res =  super().create(vals_list)
        print(vals_list)
        print(res.move_type)
        return res 


              
class AccountMoveLine(models.Model):
    
    _inherit = 'account.move.line'
    
    is_custom_paid_invoice = fields.Boolean(string="Is custom paid Invoice", default=False)
    
    @api.model_create_multi
    def create(self, vals_list):
        res =  super().create(vals_list)
        print(vals_list)
        print(res)
        return res
    
    #not using super call
    # 0: {'debit_values': None, 'credit_values': None, 'partial_values': {'amount': 10464.04, 'debit_amount_currency': 10464.04, 'credit_amount_currency': 10464.04, 'debit_move_id': 278, 'credit_move_id': 322}}
    # after super call
    # 0: {'debit_values': None, 'credit_values': None, 'partial_values': {'amount': 10464.04, 'debit_amount_currency': 10464.04, 'credit_amount_currency': 10464.04, 'debit_move_id': 278, 'credit_move_id': 322}}
    def _prepare_reconciliation_plan(self, plan, aml_values_map):
        plan_results = super()._prepare_reconciliation_plan(plan, aml_values_map)
        for rec in self:
            if rec.is_custom_paid_invoice:
                for result in plan_results:
                    partials = result.get('partial_values')
                    if partials:
                        debit_move_line_id = partials.get('debit_move_id')
                        debit_move_line = self.env['account.move.line'].browse(debit_move_line_id)
                        #invoice_line = self.payment_id.customer_invoices.filtered(lambda inv: any(line.credit > 0 and line.move_id.id == credit_move_line.move_id.id for line in inv.invoice_id.line_ids))
                        """ invoice_line = False
                        for inv in self.payment_id.customer_invoices:
                            for line in inv.invoice_id.line_ids:
                                if line.id == debit_move_line.id and line.debit > 0:
                                    invoice_line = inv
                                    break
                            if invoice_line:
                                break """
                        invoice_line = self.payment_id.customer_invoices.filtered(lambda inv: any(line.id == debit_move_line.id and line.debit > 0 for line in inv.invoice_id.line_ids))
                        
                        if invoice_line:
                            allocation = invoice_line[0].allocation_amount
                            partials['amount'] = allocation
                            partials['debit_amount_currency'] = allocation
                            partials['credit_amount_currency'] = allocation

        return plan_results


class AccountPartialReconcile(models.Model):
    
    _inherit = 'account.partial.reconcile'
    
    @api.model_create_multi
    def create(self, vals_list):
        res =  super().create(vals_list)
        return res 


