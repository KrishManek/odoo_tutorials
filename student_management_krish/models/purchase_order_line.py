# -*- coding: utf-8 -*-

from odoo import fields, models,api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    lot_name = fields.Char("Lot Name", help="Lot name")
    is_editable = fields.Boolean(string="Is lot name editable", default = False, help="used to check if product is tracking by lot")
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        """
        updates is editable based on product tracking type
        """
        if self.product_id.tracking == 'lot':
            self.is_editable = True
        else:
            self.is_editable = False
        
    