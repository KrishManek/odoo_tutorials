from odoo import models, fields, api

class LoanApprovalLevel(models.Model):
    _name = 'loan.approval.level'
    _description = 'Loan Approval Level'

    loan_id = fields.Many2one('loan.management', string='Loan', ondelete='cascade')
    level = fields.Integer(string='Level')
    name = fields.Char(string='Level Name')
    user_ids = fields.Many2many('res.users', string='Approvers', domain="[('id', 'not in', already_assigned_user_ids)]")
    already_assigned_user_ids = fields.Many2many('res.users', compute='_compute_user_domain', store=False)
    stage = fields.Selection([
        ('pending', 'Pending'),
        ('to_approve','To Approve'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')], default='pending', string='Status')
    approved_by = fields.Many2one('res.users', string='Approved By')
    rejected_by = fields.Many2one('res.users', string='Rejected By')
    timestamp = fields.Datetime(string='Timestamp')
    can_approve = fields.Boolean(compute='_compute_can_approve')

    @api.depends('user_ids', 'stage')
    def _compute_can_approve(self):
        current_user = self.env.user
        for rec in self:
            rec.can_approve = (
                rec.stage == 'to_approve' and
                current_user in rec.user_ids
            )
    
    @api.depends('user_ids')
    def _compute_user_domain(self):
        for rec in self:
            if rec.loan_id:
                other_levels = rec.loan_id.loan_approval_level_ids.filtered(lambda l: l.id != rec.id)
                other_user_ids = other_levels.mapped('user_ids').ids
                rec.already_assigned_user_ids = [(6, 0, other_user_ids)]
            else:
                rec.already_assigned_user_ids = [(6, 0, [])]         
                
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            loan_id = vals.get('loan_id')
            level = vals.get('level')
            if loan_id and level:
                if level == 1:
                    vals['stage'] = 'to_approve'
                else:
                    vals['stage'] = 'pending'
        return super().create(vals_list)
    
    def action_approve_application(self):
        for rec in self:
            approver_users = rec.user_ids
        if self.env.user in approver_users:
            rec.stage = 'approved'
            rec.approved_by = self.env.user
            rec.timestamp = fields.Datetime.now()
        
            loan = rec.loan_id
            next_level = loan.loan_approval_level_ids.filtered(lambda l: l.level == rec.level + 1 and l.stage == 'pending')
            if next_level:
                next_level.stage = 'to_approve'
            else:
                loan.state = 'approved'
    
    def action_reject_application(self):
        self.stage = 'rejected'
        self.rejected_by = self.env.uid
        self.loan_id.state = 'rejected'
        self.timestamp = fields.Datetime.now()