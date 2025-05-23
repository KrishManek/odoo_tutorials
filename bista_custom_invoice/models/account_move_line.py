from odoo import fields, models,api
from odoo.exceptions import UserError, ValidationError


class AccountMoveLine(models.Model):
    
    _inherit = 'account.move.line'
    
    is_custom_paid_invoice = fields.Boolean(string="Is custom paid Invoice", default=False)

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

