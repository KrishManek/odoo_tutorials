from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('to_approve', 'To approve'), ('sale', '')])
        
    def button_approve(self, force=False):
        orders = self.filtered(lambda order: order._approval_allowed() and order.state in ['draft', 'sent', 'to_approve'])
        if orders:
            super(SaleOrder, orders).action_confirm()

    def _confirmation_error_message(self):
        self.ensure_one()
        
        if self.state not in {'draft', 'sent', 'to_approve'}:
            return("Some orders are not in a state requiring confirmation.")

        if any(
            not line.display_type
            and not line.is_downpayment
            and not line.product_id
            for line in self.order_line
        ):
            return("A line on these orders is missing a product, you cannot confirm it.")

        return False

    def _approval_allowed(self):
        """Returns whether the order qualifies to be approved by the current user"""
        self.ensure_one()
        return (
            self.company_id.so_double_validation == 'one_step'
            or (self.company_id.so_double_validation == 'two_step'
                and self.amount_total < self.env.company.currency_id._convert(
                    self.company_id.so_double_validation_amount, self.currency_id, self.company_id,
                    self.date_order or fields.Date.today()))
            or self.env.user.has_group('sales_team.group_sale_manager')
        )
        
    def action_confirm(self):
        for order in self:
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to_approve'})
                
        