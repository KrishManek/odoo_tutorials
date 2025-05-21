from odoo import models, fields,api


class UpdateProduct(models.TransientModel):
    _name = 'update.product'

    mrp_id = fields.Many2one('mrp.production',string="MO Id")
    wizard_id = fields.Many2one('update.product.serial',string="Wizard id")
    current_product = fields.Many2one('product.product', string="Current Product")
    new_product = fields.Many2one('product.product', string="New Product")
    state = fields.Char(string="State")
        
    