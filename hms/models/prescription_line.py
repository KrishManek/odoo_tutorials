from odoo import models,fields,api


class HmsPrescriptionLine(models.Model):
    _name = "hms.prescription.line"
    _description = "Prescription Line"
    _res_name = "prescription_id.patient_id"

    prescription_id = fields.Many2one('hms.prescription', string="ID")
    product_id = fields.Many2one('product.product', string="Product", required=True, ondelete='cascade')
    qty = fields.Integer(string="Quantity", required=True, store=True)
    price_unit = fields.Float(string="Unit Price", readonly=True, required=True, store=True)
    sub_total = fields.Float(string="Total",compute = "_compute_total", readonly=True, store=True) 

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.price_unit = self.product_id.lst_price

    @api.depends('qty', 'price_unit')
    def _compute_total(self):
        for line in self:
            line.sub_total = line.qty * line.price_unit

