from email.policy import default

from odoo import fields, models, api
from odoo.fields import first


class PrescriptionLine(models.Model):
    _name = 'prescription_line.details'
    _description = 'Prescription Line Information'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product',string='Product',required=True)
    qty = fields.Integer(string='Quantity',default=1,required=True)
    price_unit = fields.Float(string='Unit Price')
    total = fields.Float(string='Total',compute='_compute_total',store=True)

    prescription_id = fields.Many2one('prescription_details','Prescription')

    @api.depends('qty', 'price_unit')
    def _compute_total(self):
        for record in self:
            record.total = record.qty * record.price_unit