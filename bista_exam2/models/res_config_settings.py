# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_approval = fields.Boolean(string="Sale Order Approval", config_parameter="bista_exam2.sale_approval")
    sale_min_amount = fields.Float(string="Minimum Amount", readonly=False, config_parameter="bista_exam2.sale_min_amount")
    