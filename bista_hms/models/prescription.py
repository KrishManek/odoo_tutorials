from odoo import models, fields, api


class HmsPrescription(models.Model):
    _name = "hms.prescription"

    patient_id = fields.Many2one("res.patient", string="Patient", required=True, ondelete="restrict")
    date = fields.Date(string="Date", required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('cancel', 'Cancel')],
                             string="Status", default='draft')
    prescription_lines = fields.One2many("prescription.line",
                                         "prescription_id", string="Prescription Lines")
    total_amount = fields.Float(compute='_compute_total_amount', string="Total Amount")

    @api.depends('prescription_lines.total')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.prescription_lines.mapped('total'))

class PrescriptionLine(models.Model):
    _name = "prescription.line"

    prescription_id = fields.Many2one("hms.prescription", string="Prescription", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Medicine", required=True)
    quantity = fields.Integer(string="Quantity", required=True)
    price_unit = fields.Float(string="Price Unit", required=True)
    total = fields.Float(string="Total", compute="_compute_total", store=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.price_unit = self.product_id.lst_price

    @api.depends('quantity', 'price_unit')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.price_unit