from odoo import models, fields,api
from odoo.exceptions import ValidationError


class AddDocWizard(models.TransientModel):
    _name = 'add.document'
    _description = 'Add Docs'
    
    sale_id = fields. Many2one('sale.order', string="Order_id", compute="_get_sale_id")
    product_ids = fields.Many2many('product.product', string="Products")
    
    def _get_sale_id(self):
        for rec in self:
            rec.sale_id = self._context.get('active_id')   
         
    def action_add_docs(self):
        self.sale_id = self._context.get('active_id')
        if self.sale_id:
            sale_lines = []
            for product in self.product_ids:
                if product:
                    sale_lines.append((0, 0, {
                        'product_id': product.id,
                        'product_uom_qty': 1,
                    }))
            self.sale_id.order_line = sale_lines