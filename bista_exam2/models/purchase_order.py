from odoo import fields,models,api
from odoo.exceptions import UserError

class Product(models.Model):
    _inherit = 'purchase.order'
    
    def button_confirm(self):
        result = super().button_confirm()
        if self.partner_id.email:
            template_id = self.env.ref('bista_exam2.email_template_new_purchase_order')
            template_id.send_mail(self.id)
        return result
    
    