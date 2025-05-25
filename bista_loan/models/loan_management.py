from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class LoanManagement(models.Model):
    _name = 'loan.management'
    _rec_name = 'partner_id'

    loan_amount = fields.Float(string="Loan Amount", default=10000)
    partner_id = fields.Many2one('res.partner', string="Partner")
    user_id = fields.Many2one('res.users', string="User", domain="[('id','!=', uid)]")
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
    
    approval_team = fields.Many2one('approval.team', string="Aprroval Team")
    state = fields.Selection([('draft', 'Draft'),
                              ('to_approve', 'Approve'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejcted')], string="Status", default='draft')
    
    loan_approval_level_ids = fields.One2many('loan.approval.level', 'loan_id', string="Loan Approval Levels")
    next_approvers = fields.Many2many('res.users', string = "Next Approvers", compute= "_compute_next_approvers", store=True)
    
    advance_payments = fields.One2many('advance.payment', 'loan_id')
    #is_advance_payment = fields.Boolean(string="Is advance_payment", default=False)
    
    
    @api.depends('loan_approval_level_ids.stage')
    def _compute_next_approvers(self):
        for rec in self:
            approvers = rec.loan_approval_level_ids.filtered(lambda lvl: lvl.stage == 'pending').mapped('user_ids')
            if approvers:
                rec.next_approvers = approvers
            else:
                rec.next_approvers = [(5, 0, 0)]
            
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('user_id'):
                vals['user_id'] = self.env.uid
            vals['state'] = 'to_approve' 
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
        
    @api.depends('rate_of_interests.rate', 'rate_of_interests.is_active', 'loan_amount', 'period', 'advance_payments.status', 'emi_line_ids.state')    
    def _compute_emi(self):
        for rec in self:
            rate = rec.rate_of_interest
            if rate and rec.period > 0 and rec.loan_amount >= 1000:
                paid_principal_emi = sum(rec.emi_line_ids.filtered(lambda l: l.state == 'paid').mapped('principle_amount'))
                paid_advance = sum(rec.advance_payments.filtered(lambda p: p.status == 'paid').mapped('amount'))
                remaining_principal = rec.loan_amount - paid_principal_emi - paid_advance

                monthly_interest_rate = rate / 1200
                n = rec.period - len(rec.emi_line_ids.filtered(lambda l: l.state in ['paid', 'invoiced']))

                if n > 0 and remaining_principal > 0:
                    rec.emi_amount = ((remaining_principal * monthly_interest_rate) /(1 - (1 / (1 + monthly_interest_rate) ** n)))
                    month = 1
                    amount_current = remaining_principal * (1 + monthly_interest_rate) ** month
                    amount_previous = remaining_principal * (1 + monthly_interest_rate) ** (month - 1)
                    interest_this_month = amount_current - amount_previous
                    rec.monthly_intrest = interest_this_month
                else:
                    rec.emi_amount = 0.0
                    rec.monthly_intrest = 0.0

                    
    @api.depends('emi_line_ids.state', 'advance_payments.status')
    def _compute_amounts(self):
        for rec in self:
            emi_lines = rec.emi_line_ids
            paid_emi_lines = emi_lines.filtered(lambda r: r.state == 'paid')
            total_interest = sum(emi_lines.mapped('interest_amount'))
            paid_interest = sum(paid_emi_lines.mapped('interest_amount'))
            paid_principal_emi = sum(paid_emi_lines.mapped('principle_amount'))
            paid_advance_amount = sum(rec.advance_payments.filtered(lambda p: p.status == 'paid').mapped('amount'))
            total_paid_principal = paid_principal_emi + paid_advance_amount
            rec.total_principle_amount = rec.loan_amount
            rec.total_interest_amount = total_interest
            rec.interest_amount = paid_interest
            rec.principle_amount = total_paid_principal
            rec.pending_principle_amount = rec.loan_amount - total_paid_principal
            rec.pending_interest_amount = total_interest - paid_interest
    
    def create_emi_lines(self):
        for rec in self:
            pending_lines = rec.emi_line_ids.filtered(lambda l: l.state == 'pending')
            pending_lines.unlink()

            # Calculate already paid principal from EMI and advance payments
            paid_principal_emi = sum(rec.emi_line_ids.filtered(lambda l: l.state == 'paid').mapped('principle_amount'))
            paid_advance = sum(rec.advance_payments.filtered(lambda p: p.status == 'paid').mapped('amount'))

            total_paid_principal = paid_principal_emi + paid_advance
            remaining_principal = rec.loan_amount - total_paid_principal
            monthly_rate = rec.rate_of_interest / 1200
            emi_date = rec.next_emi_date or rec.emi_date
            paid_or_invoiced = rec.emi_line_ids.filtered(lambda l: l.state in ['paid', 'invoiced'])
            remaining_periods = rec.period - len(paid_or_invoiced)
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
        invoice = self._prepare_invoice_vals(rec)
        invoice_id = self.env['account.move'].create(invoice)
        emi_line=self.prepare_invoice_line_vals(invoice_id, rec)
        line_ids=self.env['account.move.line'].create(emi_line)
        invoice_id.action_post() 
        return True
        
    def _prepare_invoice_vals(self, rec):
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
        product = product_template.product_variant_id.id
        if not product:
            raise UserError("Product 'EMI' not found. Please configure it in Products.")
        line_vals_list = []
        line_vals = {
            'product_id': product,
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
        
    def action_approve_application(self):
        self.state = 'to_approve'
    
    def action_reject_application(self):
        self.state = 'rejected'
        
    @api.onchange('approval_team')
    def _onchange_approval_team(self):
        for rec in self:
            rec.loan_approval_level_ids = [(5, 0, 0)]
            if rec.approval_team:
                assigned_users = set()
                level_vals = []

                for level in rec.approval_team.approval_level_ids:
                    """ unique_user_ids = [u.id for u in level.user_ids if u.id not in assigned_users]
                    if unique_user_ids: """
                    level_vals.append((0, 0, {
                        'level': level.level,
                        'name': level.name,
                        'user_ids': [(6, 0, level.user_ids.ids)],
                    }))
                        #assigned_users.update(unique_user_ids)

                rec.loan_approval_level_ids = level_vals