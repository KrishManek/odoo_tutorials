from odoo import api, fields, models
from odoo.exceptions import UserError


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    
    full_payment_enforcement_warning = fields.Html(compute="_compute_only_full_payment_warning",readonly=True,string="",)

    
    @api.depends('amount', 'currency_id', 'line_ids')
    def _compute_only_full_payment_warning(self):
        for wizard in self:
            moves_with_loan = wizard.line_ids.mapped('move_id').filtered(lambda move: move.loan_id)
            if moves_with_loan:
                totals = wizard._get_total_amounts_to_pay(wizard.batches)
                full_amount = totals.get('full_amount', 0.0)
                if not wizard.currency_id.is_zero(wizard.amount - full_amount):
                    wizard.full_payment_enforcement_warning = "<div class='alert alert-danger'> Full payment is required because the invoice is linked to a loan.</div>"
                else:
                    wizard.full_payment_enforcement_warning = ""
            else:
                wizard.full_payment_enforcement_warning = ""

                
    def action_create_payments(self):
        for wizard in self:
            # Only care about invoices that are loan-linked
            moves_with_loan = wizard.line_ids.mapped('move_id').filtered(lambda move: move.loan_id)
            if moves_with_loan:
                totals = wizard._get_total_amounts_to_pay(wizard.batches)
                full_amount = totals.get('full_amount', 0.0)
                if not wizard.currency_id.is_zero(wizard.amount - full_amount):
                    raise UserError("This invoice is linked to a loan. Only full payments are allowed.")
        return super().action_create_payments()
    
    
    def _create_payments(self):
        res = super()._create_payments()
        if res:
            for wizard in self:
                moves_with_loan = wizard.line_ids.mapped('move_id').filtered(lambda move: move.loan_id)
                if moves_with_loan:
                    for move in moves_with_loan:
                        invoiced_date = move.invoice_date
                        emi_lines = move.loan_id.emi_line_ids.filtered(lambda emi: emi.paid_date == invoiced_date)
                        emi_lines.write({'state': 'paid'})
                        advance_payment_lines = move.loan_id.advance_payments.filtered(lambda pay: pay.paid_date == invoiced_date)
                        advance_payment_lines.write({'status': 'paid'})
                        if advance_payment_lines:
                            moves_with_loan.loan_id.create_emi_lines()
        return res                

    
    