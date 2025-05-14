import math
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
            rec.end_date = self.start_date + relativedelta(months=self.period)
        
    @api.depends('rate_of_interests.rate','rate_of_interests.is_active','loan_amount','period')    
    def _compute_emi(self):
        rate = self.env['interest.rate'].search([('is_active', '=', True),
                                                 ('loan_id', '=', self.id)], limit=1).mapped('rate')
        if rate:
            if self.period > 0 and self.loan_amount >= 1000 and rate[0] > 0:
                for rec in self:
                    monthly_interest_rate = rate[0] / 1200
                    n = rec.period
                    self.emi_amount = ((rec.loan_amount * monthly_interest_rate) /(1 - (1 / (1 + monthly_interest_rate) ** n)))
                    month = 1
                    amount_current = rec.loan_amount * (1 + monthly_interest_rate) ** month
                    amount_previous = rec.loan_amount * (1 + monthly_interest_rate) ** (month - 1)
                    interest_this_month = ((amount_current - amount_previous))
                    self.monthly_intrest = interest_this_month
                        
                    """  monthly_interest_rate = rate[0] / 1200
                    #monthly_interest_rate = rec.rate_of_interest / 1200
                    n = rec.period
                    self.emi_amount = math.ceil((rec.loan_amount * monthly_interest_rate) / (1 - (1 / (1 + monthly_interest_rate) ** n)))
                    # Formula for compund interest
                    # (rec.loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**rec.period) / ((1 + monthly_interest_rate)**rec.period - 1)
                    self.monthly_intrest = rec.loan_amount * monthly_interest_rate * 1 """
                    
    @api.depends('emi_line_ids')    
    def _compute_amounts(self):
        for rec in self:
            rec.total_principle_amount = rec.loan_amount
            data = self.env['emi.line'].search([('loan_id','=', rec.id)])
            interest = sum(data.mapped('interest_amount'))
            principle = sum(data.mapped('principle_amount'))
            rec.total_interest_amount = interest
            rec.interest_amount = interest
            rec.principle_amount = principle
            rec.pending_principle_amount = rec.loan_amount  - principle
    
    def create_emi_lines(self):
        # create emi lines
        # EMI = [P * r * (1 + r)^N] / [(1 + r)^N - 1]
        previous_unpaid_amount = self.loan_amount
        monthly_rate = (self.rate_of_interest / 1200)
        self.emi_line_ids = [(5, 0, 0)]
        vals = []
        emi_date = self.emi_date
        for line in range(self.period):
            interest_charged = (monthly_rate * previous_unpaid_amount)
            principal_paid = (self.emi_amount - interest_charged)
            total_payment = (interest_charged + principal_paid)
            vals.append((0, 0, ({
                'principle_amount': principal_paid,
                'interest_amount': interest_charged,
                'total_paid': total_payment,
                'paid_date': emi_date,
                'loan_id': self.id,
            })))

            previous_unpaid_amount = previous_unpaid_amount - principal_paid
            emi_date = emi_date + relativedelta(months=1)
        self.emi_line_ids = vals
        """ rate = self.env['interest.rate'].search([('is_active', '=', True),
                                                 ('loan_id', '=', self.id)], limit=1).mapped('rate')
        if rate:
            if self.period > 0 and self.loan_amount >= 1000 and rate[0] > 0:
                    monthly_interest_rate = rate[0] / 1200
                    n = self.period
                    self.emi_line_ids = [(5, 0, 0)]
                    for curr_month in range(n):
                        amount_current = self.loan_amount * (1 + monthly_interest_rate) ** (curr_month + 1)
                        amount_previous = self.loan_amount * (1 + monthly_interest_rate) ** (curr_month)
                        date = self.emi_date + relativedelta(months=curr_month)
                        interest_this_month = math.ceil(amount_current - amount_previous)
                        principle = self.emi_amount - interest_this_month
                        self.emi_line_ids = [(0,0, {'paid_date': date,
                                           'interest_amount': interest_this_month,
                                           'principle_amount': principle,
                                           'loan_id': self.id,
                                           'total_paid': principle + interest_this_month
                                           })] """

    def pay_emi(self):
        data = self.search([])
        today = fields.Date.today()
        for rec in data:
            line = rec.emi_line_ids.filtered(lambda line: line.paid_date== today)
            if rec.action_create_invoice():
                line.state = 'invoiced'
                rec._send_mail_to_loan_partner()
            """ for invoice in invoices:
                invoice.action_post() """

    def action_create_invoice(self):
        invoice = self._prepare_invoice()
        create_invoice = self.env['account.move'].create(invoice)
        emi_line=self.prepare_invoice_line_vals(create_invoice)
        line_ids=self.env['account.move.line'].create(emi_line)
        create_invoice.action_post() 
        return True
        

    def _prepare_invoice(self):
        today = fields.date.today()
        value = {
            'partner_id': self.partner_id.id,
            'partner_shipping_id': self.partner_id.id,
            'move_type':'out_invoice',
            'invoice_user_id': self.env.user.id,
            'company_id': self.env.user.company_id.id,
            'invoice_date': self.emi_date,
            'user_id': self.env.user.id,
            'loan_id': self.id,
        }
        return value

    def prepare_invoice_line_vals(self,create_invoice):
        product_id = self.env['product.product'].search([('name','=','EMI')])
        line_vals_list = []
        line_vals = {
            'product_id': product_id.id,
            'quantity': 1,
            'price_unit': self.emi_amount,
            'discount': 0.0,
            'move_id': create_invoice.id,
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