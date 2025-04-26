from odoo import fields, models

class DocumentsCustom(models.Model):
    _name = 'documents.custom'
    _description = 'Custom Documents'
    
    name = fields.Char(string="Name")
    attachment_id = fields.Many2one('ir.attachment', string="Attachment")
    doc_tag_ids = fields.Many2many('doc.tag.master', string="Tags")