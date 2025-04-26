from odoo import models, fields, api
from datetime import datetime, timedelta

class SaleOrderReminder(models.Model):
    _inherit = 'sale.order'

    def send_expiry_reminder(self):
        param = self.env['ir.config_parameter'].sudo()

        if param.get_param('bista_sales.expiry_reminder') != 'True':
            return 

        ex_days = int(param.get_param('bista_sales.quote_expiry_days', 3))
        target_date = self.validity_date - timedelta(days=ex_days)

        expiring_quotes = self.search([('state', '=', 'sent'),('validity_date', '=', target_date),('validity_date', '=', target_date)])
        
