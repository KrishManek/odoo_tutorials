from odoo import fields, models,api
from odoo.exceptions import ValidationError

class DocTagMaster(models.Model):
    _name = 'doc.tag.master'
    _description = 'Document Tag Master'
    
    name = fields.Char(string="Name")
    