from odoo import fields,models,api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        res =  super().create(vals_list)
        return res
    