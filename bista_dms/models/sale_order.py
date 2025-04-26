from odoo import fields,models,api
from odoo.exceptions import UserError
class SaleOrder(models.Model):
    _inherit = 'sale.order'


    doc_tag_ids = fields.Many2many('doc.tag.master', string="Document Tags")
    document_ids = fields.Many2many('documents.custom', string="Documents")
    compute_docs = fields.Integer(string="Total Docs", compute='_compute_documents', store=True)
    doc_line_ids = fields.One2many('documents.order.line','sale_id',string="Document Line Id ")
    allow_upd = fields.Boolean(string="Allow update", compute="_compute_allowed", default=False)
    """ @api.onchange('document_ids')
    def _onchange_doc(self):
        if self.order_line: 
            lines = []
            self.doc_line_ids = [(5, 0, 0)] 
            for doc in self.document_ids:
                lines.append((0, 0, {'document_id':doc.id}))
            self.doc_line_ids = lines
    
    @api.depends('document_ids')
    def _compute_documents(self):
        for rec in self:
            rec.compute_docs = len(rec.document_ids) """
    
    def _compute_allowed(self):
        self.ensure_one()
        for rec in self:
            allowed_update = self.env['ir.config_parameter'].sudo().get_param('allow_update_doc_after_confirm')
            if allowed_update == 'True':
                rec.allow_upd = True
            else:
                rec.allow_upd = False
    @api.onchange('partner_id')
    def _onchange_partner_id_tags(self):
        if self.partner_id:
            self.doc_tag_ids = [(6, 0, self.partner_id.tag_ids.ids)]
            
    """ def button_get_docs(self):
        docs = self._collect_documents_by_tags()
        lines = []
        self.doc_line_ids = [(5, 0, 0)]
        for doc in docs: 
            for order in self.order_line:
                product = order.product_id
                 
            lines.append((0, 0, {'document_id':doc.id}))  
        self.doc_line_ids = lines
        #self.document_ids = [(6, 0, docs.ids)]
        
 """
    def button_get_docs(self):
        tags = self.doc_tag_ids.ids
        docs = self.env['documents.custom']
        lines = []
        self.doc_line_ids = [(5,0,0)]
        for order in self.order_line:
            filtered_docs = order.product_id.document_ids.filtered(lambda o: any(tag.id in tags for tag in o.doc_tag_ids))
            docs |= filtered_docs
        #code form here
            
            for doc in docs:
                if any(item[2].get('document_id') == doc.id for item in lines):
                    for item in lines:
                        item[2]['product_ids'] += order.product_id 
                else:
                    lines.append((0,0,{
                        'document_id':doc.id,
                        'product_ids': order.product_id,
                    }))
        self.document_ids = [(6, 0, docs.ids)]
        self.doc_line_ids = lines
        if self.user_id.email_formatted:
            template_id = self.env.ref('bista_dms.email_template_sale_order')
            template_id.send_mail(self.id)
        self.message_post(body=f"Hi, This order is created by {self.env.user.name}.")
        
    def _collect_documents_by_tags(self):
        tags = self.doc_tag_ids.ids
        docs = self.env['documents.custom']
        for order in self.order_line:  
            product_docs = order.product_id.document_ids
            filtered = product_docs.filtered(lambda o : any(tag.id in tags for tag in o.doc_tag_ids))
            docs |= filtered
        return docs
    
    def button_update_docs(self):
        self.ensure_one()
        """ if self.state != 'sale' and not self.allow_upd:
            return
        existing_docs = self.document_ids
        new_docs = self.button_get_docs()
        added_docs = new_docs - existing_docs
        if added_docs:
            self.picking_ids.document_ids = self.document_ids """
        self.message_post(body=f"Hi, This order is created by {self.user_id.name}.")
        """ new_docs = self._collect_documents_by_tags()
        combined_docs = (self.document_ids | new_docs).filtered(lambda d: d not in self.document_ids)
        if combined_docs:
            self.document_ids |= combined_docs
            self.picking_ids.document_ids = self.document_ids """
    
    def action_confirm(self):
        super().action_confirm()
        self.picking_ids.document_ids = self.document_ids
        
    def button_add_docs(self):
        veiw_id = self.env.ref("bista_dms.view_add_doc_wizard").id
        return {
            'name' : "return Window",
            'view_mode' : "form",
            'res_model' : 'add.document',
            'view_id' : veiw_id,
            'type' : "ir.actions.act_window",
            'target' : 'new',
            'context': {'default_sale_id': self.id}
        }