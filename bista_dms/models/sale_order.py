from odoo import fields,models,api
from odoo.exceptions import UserError
class SaleOrder(models.Model):
    _inherit = 'sale.order'


    doc_tag_ids = fields.Many2many('doc.tag.master', string="Document Tags")
    document_ids = fields.Many2many('documents.custom', string="Documents")
    
    @api.onchange('partner_id')
    def _onchange_partner_id_tags(self):
        if self.partner_id:
            self.doc_tag_ids = [(6, 0, self.partner_id.tag_ids.ids)]
            
    def button_get_docs(self):
        docs = self._collect_documents_by_tags()
        self.document_ids = [(6, 0, docs.ids)]

    
    def _collect_documents_by_tags(self):
        tags = self.doc_tag_ids.ids
        docs = self.env['documents.custom']
        for order in self.order_line:  
            product_docs = order.product_id.document_ids
            filtered = product_docs.filtered(lambda o : any(tag.id in tags for tag in o.doc_tag_ids))
            docs |= filtered
        return docs
    
    def button_update_docs(self):
        if self.state != 'sale':
            return
        new_docs = self._collect_documents_by_tags()
        combined_docs = (self.document_ids | new_docs).filtered(lambda d: d not in self.document_ids)
        if combined_docs:
            self.document_ids |= combined_docs
            self.picking_ids.document_ids = self.document_ids
    
    def action_confirm(self):
        super().action_confirm()
        self.picking_ids.document_ids = self.document_ids