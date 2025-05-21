from odoo import models, fields,api


class UpdateSerial(models.TransientModel):
    _name = 'update.serial'

    mrp_id = fields.Many2one('mrp.production',string="MO Id")
    wizard_id = fields.Many2one('update.product.serial',string="Wizard id")
    current_product = fields.Many2one('product.product', string="Current Product")
    old_serial =fields.Char(string="Old Serial code")
    new_serial =fields.Char(string="New Serial code")
        
    