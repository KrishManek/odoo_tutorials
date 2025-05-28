from odoo import fields,models,api
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        result = super().button_confirm()
        for order in self:
            if order.partner_id.email:
                template_id = self.env.ref('bista_exam2.email_template_new_purchase_order')
                template_id.send_mail(self.id, force_send=True)
            if order.state == 'to approve':
                group_id = self.env.ref('bista_exam2.group_purchase_approver').id
                approver_users = self.env['res.users'].search([('groups_id', 'in', group_id)])
                template_id = self.env.ref('bista_exam2.po_approval_email_template_view')
                for user in approver_users:
                    email_values = {'email_to' : user.email} 
                    template_id.with_context({'user_name':user.name}).send_mail(self.id, force_send=True, email_values=email_values)
        return result
    
    def get_approver_users(self):
        approver_users = self.env['res.users'].search([
            ('groups_id', 'in', self.env.ref('bista_exam2.group_purchase_approver').id)
        ])
        return approver_users.mapped('name')
        
    def _approval_allowed(self):
        """Returns whether the order qualifies to be approved by the current user"""
        self.ensure_one()
        return (
            self.company_id.po_double_validation == 'one_step'
            or (self.company_id.po_double_validation == 'two_step'
                and self.amount_total < self.env.company.currency_id._convert(
                    self.company_id.po_double_validation_amount, self.currency_id, self.company_id,
                    self.date_order or fields.Date.today()))
            or self.env.user.has_group('bista_exam2.group_purchase_approver'))
    