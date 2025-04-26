from odoo import fields, models

class DocumentsOrderLine(models.Model):
    _name = 'documents.order.line'
    _description = 'Custom Order Line '
    _rec_name = 'sale_id'
    
    sale_id = fields.Many2one('sale.order', string="Sale Order")
    document_id = fields.Many2one('documents.custom', string="Documents")
    product_ids = fields.Many2many('product.product', string="Products")