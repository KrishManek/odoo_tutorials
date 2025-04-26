from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    credit_card = fields.Char(string="Credit Card")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            card_no = self.env.context.get('credit_card')
            if card_no:
                vals['credit_card'] = card_no
        res = super(AccountPayment, self).create(vals_list)
        return res