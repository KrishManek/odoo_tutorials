from odoo import models, fields, api


class AdvancePayment(models.Model):
    _name = 'advance.payment'
    _rec_name = 'amount'
    
    loan_id = fields.Many2one('loan.management', string="Loan_id")
    amount = fields.Float(string="Advance Payment Amount", default=1)
    paid_date = fields.Date(string="Payment Date", default = fields.Date.today())
    status = fields.Selection([('draft', 'Draft'),
                               ('created', 'Created'),
                              ('paid', 'Paid')], string="Status", default='draft')
    
    def make_payment(self):
        self.action_create_invoice()
            
            
    def action_create_invoice(self):
        invoice = self._prepare_invoice_vals()
        invoice_id = self.env['account.move'].create(invoice)
        emi_line=self.prepare_invoice_line_vals(invoice_id)
        line_ids=self.env['account.move.line'].create(emi_line)
        invoice_id.action_post() 
        self.write({'status': 'created'})
        
    def _prepare_invoice_vals(self):
        today = fields.date.today()
        value = {
            'partner_id': self.loan_id.partner_id.id,
            'partner_shipping_id': self.loan_id.partner_id.id,
            'move_type':'out_invoice',
            'invoice_user_id': self.env.user.id,
            'company_id': self.env.user.company_id.id,
            'invoice_date': self.paid_date,
            'user_id': self.env.user.id,
            'loan_id': self.loan_id.id,
        }
        return value

    def prepare_invoice_line_vals(self,invoice_id):
        line_vals_list = []
        line_vals = {
            'quantity': 1,
            'price_unit': self.amount,
            'discount': 0.0,
            'move_id': invoice_id.id,
            'tax_ids': [],
            }
        line_vals_list.append(line_vals)
        return line_vals_list