from odoo import fields, models,api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        return res
    
    def _prepare_picking(self):
        res = super()._prepare_picking()
        res.update({
            'location_dest_id' : self.order_line.location_final_id.id
        })
        return res