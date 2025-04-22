from odoo import fields,models,api
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    tag_ids = fields.Many2many('doc.tag.master', string="Document Tags")
     