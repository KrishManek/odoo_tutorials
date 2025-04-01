from odoo import models, fields, api

# Define the HmsPrescriptionLine model
class HmsPrescriptionLine(models.Model):
    _name = "hms.prescription.line"  # Model name
    _description = "Prescription Line"  # Model description
    _res_name = "prescription_id.patient_id"  # Field used for record name

    # Define fields for the model
    prescription_id = fields.Many2one('hms.prescription', string="ID")  # Reference to prescription
    product_id = fields.Many2one('product.product', string="Product", required=True, ondelete='cascade')  # Reference to product
    qty = fields.Integer(string="Quantity", required=True, store=True)  # Quantity of the product
    price_unit = fields.Float(string="Unit Price", readonly=True, required=True, store=True)  # Unit price of the product
    sub_total = fields.Float(string="Total", compute="_compute_total", readonly=True, store=True)  # Computed field for total amount
    move_ids = fields.One2many("stock.move", 'prescription_line_id', string="Prescription")

    # On change event to update unit price based on selected product
    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.price_unit = self.product_id.lst_price

    # Compute the total amount of the prescription line
    @api.depends('qty', 'price_unit')
    def _compute_total(self):
        for line in self:
            line.sub_total = line.qty * line.price_unit