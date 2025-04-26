from odoo import models, api


class AccountRegisterPayment(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        return super(AccountRegisterPayment, self.with_context(credit_card=12345)).action_create_payments()