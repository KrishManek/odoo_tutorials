from odoo import models, api, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    lead_referral = fields.Char(string="Lead Referral")


