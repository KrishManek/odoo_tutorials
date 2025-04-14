# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    
    so_order_approval = fields.Boolean("Sale Order Approval", default=lambda self: self.env.company.po_double_validation == 'two_step')
    so_double_validation = fields.Selection(related='company_id.so_double_validation', string="Levels of Approvals *", readonly=False)
    so_double_validation_amount = fields.Monetary(related='company_id.so_double_validation_amount', string="Minimum Amount", currency_field='company_currency_id', readonly=False)
    
    """ def set_values(self):
        super().set_values()
        so_double_validation = 'two_step' if self.so_order_approval else 'one_step'
        if self.so_double_validation != so_double_validation:
            self.o_double_validation = so_double_validation """
    def set_values(self):
        super().set_values()
        self.company_id.so_double_validation = 'two_step' if self.so_order_approval else 'one_step'

