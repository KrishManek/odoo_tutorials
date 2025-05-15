from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class LoanManagement(models.Model):
    _name = 'loan.management'
    _rec_name = 'partner_id'

    loan_amount = fields.Float(string="Loan Amount", default=10000)
    partner_id = fields.Many2one('res.partner', string="Partner")
    user_id = fields.Many2one('res.users', string="User")
    period = fields.Integer(string="No of Months.", default = 1)
    start_date = fields.Date(string="Start Date.", default = fields.Date.today())
    end_date = fields.Date(string="End Date.", compute = "_compute_end_date", store=True)
    emi_amount = fields.Float(string="Emi Amount", compute ="_compute_emi",store=True )
    emi_date = fields.Date(string="Emi Date", default = fields.Date.today())
    rate_of_interests = fields.One2many('interest.rate', 'loan_id')
    emi_line_ids = fields.One2many('emi.line', 'loan_id')
    rate_of_interest = fields.Float(string='Rate of Interest.', default=1)
    monthly_intrest = fields.Float(string="Monthly Interest")
    
    total_interest_amount = fields.Float(string="Total Interest Amount.", compute = "_compute_amounts", store=True)
    interest_amount = fields.Float(string="Interest Amount.", compute = "_compute_amounts", store=True)
    pending_interest_amount = fields.Float(string="Pending Interest Amount.", compute = "_compute_amounts", store=True)
    total_principle_amount = fields.Float(string="Total Principle Amount.", compute = "_compute_amounts", store=True)
    principle_amount = fields.Float(string="Principle Amount.", compute = "_compute_amounts", store=True)
    pending_principle_amount = fields.Float(string="Pending Principle Amount.", compute = "_compute_amounts", store=True)
    invoice_ids = fields.One2many('account.move', 'loan_id', string="Invoices" )   
    total_invoices = fields.Integer(compute='_compute_total_invoices', store=True)
    next_emi_date = fields.Date(string="Next EMI Date")
    
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('user_id'):
                vals['user_id'] = self.env.uid
        return super(LoanManagement, self).create(vals_list)
    
    def action_open_invoices(self):
        form_view_id = self.env.ref('account.view_move_form').id 
        list_view_id = self.env.ref('account.view_out_invoice_tree').id 

        res = {
            'name': 'Invoices',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': form_view_id,
            'target': 'current',
            'context': {'default_loan_id': self.id}
        }
        if self.total_invoices >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('loan_id', '=', self.id)]
            res['view_id'] = False
        return res
    
    @api.depends('invoice_ids')
    def _compute_total_invoices(self):
        for rec in self:
            rec.total_invoices = len(rec.invoice_ids)
    
    @api.depends('start_date','period')
    def _compute_end_date(self):
        for rec in self:
            rec.end_date = rec.start_date + relativedelta(months=rec.period)
        
    @api.depends('rate_of_interests.rate','rate_of_interests.is_active','loan_amount','period')    
    def _compute_emi(self):
        for rec in self:
            rate = rec.rate_of_interest
            if rate and rec.period > 0 and rec.loan_amount >= 1000:
                monthly_interest_rate = rate / 1200
                n = rec.period
                rec.emi_amount = ((rec.loan_amount * monthly_interest_rate) /
                                (1 - (1 / (1 + monthly_interest_rate) ** n)))
                # Just for display
                month = 1
                amount_current = rec.loan_amount * (1 + monthly_interest_rate) ** month
                amount_previous = rec.loan_amount * (1 + monthly_interest_rate) ** (month - 1)
                interest_this_month = amount_current - amount_previous
                rec.monthly_intrest = interest_this_month

                    
    @api.depends('emi_line_ids.state')    
    def _compute_amounts(self):
        for rec in self:
            rec.total_principle_amount = rec.loan_amount
            data = rec.emi_line_ids
            total_interest = sum(data.mapped('interest_amount'))
            paid_lines = data.filtered(lambda r: r.state == 'paid')
            paid_interest = sum(paid_lines.mapped('interest_amount'))
            paid_principal = sum(paid_lines.mapped('principle_amount'))
            rec.total_interest_amount = total_interest
            rec.interest_amount = paid_interest
            rec.principle_amount = paid_principal
            rec.pending_principle_amount = rec.loan_amount - paid_principal
            rec.pending_interest_amount = total_interest - paid_interest
    
    def create_emi_lines(self):
        for rec in self:
            pending_lines = rec.emi_line_ids.filtered(lambda l: l.state == 'pending')
            pending_lines.unlink()
            paid_principal = sum(rec.emi_line_ids.filtered(lambda l: l.state == 'paid').mapped('principle_amount'))
            remaining_principal = rec.loan_amount - paid_principal
            monthly_rate = rec.rate_of_interest / 1200
            #emi_date = rec.emi_date
            emi_date = rec.next_emi_date or rec.emi_date
            remaining_periods = rec.period - len(rec.emi_line_ids.filtered(lambda l: l.state in ['paid', 'invoiced']))
            vals = []
            for line in range(remaining_periods):
                interest_charged = monthly_rate * remaining_principal
                emi_amount = rec.emi_amount
                principal_paid = emi_amount - interest_charged
                total_payment = interest_charged + principal_paid
                vals.append((0, 0, {
                    'principle_amount': principal_paid,
                    'interest_amount': interest_charged,
                    'total_paid': total_payment,
                    'paid_date': emi_date,
                    'loan_id': rec.id,
                }))
                remaining_principal -= principal_paid
                emi_date += relativedelta(months=1)
            rec.emi_line_ids = vals

    def generate_emi_invoices(self):
        today = fields.Date.today()
        to_invoice_today = self.env['emi.line'].search([('paid_date', '=', today)])
        for rec in to_invoice_today:
            if self.action_create_invoice(rec):
                rec.state = 'invoiced'
                self._send_mail_to_loan_partner()
                rec.loan_id.next_emi_date = rec.paid_date + relativedelta(months=1)
                
    def action_create_invoice(self, rec):
        invoice = self._prepare_invoice(rec)
        invoice_id = self.env['account.move'].create(invoice)
        emi_line=self.prepare_invoice_line_vals(invoice_id, rec)
        line_ids=self.env['account.move.line'].create(emi_line)
        invoice_id.action_post() 
        return True
        
    def _prepare_invoice(self, rec):
        today = fields.date.today()
        value = {
            'partner_id': rec.loan_id.partner_id.id,
            'partner_shipping_id': rec.loan_id.partner_id.id,
            'move_type':'out_invoice',
            'invoice_user_id': self.env.user.id,
            'company_id': self.env.user.company_id.id,
            'invoice_date': rec.paid_date,
            'user_id': self.env.user.id,
            'loan_id': rec.loan_id.id,
        }
        return value

    def prepare_invoice_line_vals(self,invoice_id, rec):
        #product_id = self.env['product.product'].search([('name','=','EMI')])
        product_template = self.env.ref('bista_loan.product_product_emi_template')
        product = product_template.product_variant_id
        if not product:
            raise UserError("Product 'EMI' not found. Please configure it in Products.")
        line_vals_list = []
        line_vals = {
            'product_id': product.id,
            'quantity': 1,
            'price_unit': rec.total_paid,
            'discount': 0.0,
            'move_id': invoice_id.id,
            'tax_ids': [],
            }
        line_vals_list.append(line_vals)
        return line_vals_list
    
    def _send_mail_to_loan_partner(self):
        template_id = self.env.ref('bista_loan.email_template_loan_emi_reminder')
        if template_id:
            template_id.send_mail(self.id, force_send=True)
        else:
            raise UserError("Mail Template not found. Please check the template.")