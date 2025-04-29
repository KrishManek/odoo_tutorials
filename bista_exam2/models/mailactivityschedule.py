from odoo import fields,models,api
from odoo.exceptions import UserError

class MailActivitySchedule(models.TransientModel):
    _inherit = 'mail.activity.schedule'
    
    meaningful_connection = fields.Boolean(string="Meaningful Connection")
    
    