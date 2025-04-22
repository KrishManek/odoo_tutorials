from odoo import fields, api, models

class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    document_ids = fields.Many2many('documents.custom',  string="Documents")
    
    # this can also be used
    """ @api.model_create_multi
    def create(self, val_list):
        picking = super().create(val_list)
        for vals in val_list:
            if picking.origin in vals:
                so = self.env['sale.order'].search([('name', '=', picking.origin)], limit=1)
                if so and so.document_ids:
                    picking.document_ids = [(6, 0, so.document_ids.ids)]
        return picking """