from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz

class HmsPrescription(models.Model):
    _name = "hms.prescription"
    _inherit = ["mail.thread", 'mail.activity.mixin']

    patient_id = fields.Many2one("res.patient", string="Patient",
                                 required=True, ondelete="restrict", tracking=1)
    date = fields.Date(string="Date", required=True, tracking=10)
    test_date = fields.Datetime(string="Test Date", tracking=10)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('cancel', 'Cancel')],
                             string="Status", default='draft')
    prescription_lines = fields.One2many("prescription.line",
                                         "prescription_id", string="Prescription Lines")
    total_amount = fields.Float(compute='_compute_total_amount', string="Total Amount")
    invoice_ids = fields.Many2many("account.move", string="Invoices")
    picking_ids = fields.Many2many("stock.picking", string="Pickings")

    def get_test_date(self):
        utc_time = self.test_date
        utc = pytz.utc
        local = self.env.user.tz
        local_tz = pytz.timezone(local)
        formated_time = utc.localize(utc_time).astimezone(local_tz)
        formated_str = fields.Datetime.to_string(formated_time)
        return formated_time


    def write(self, vals):
        res = super().write(vals)
        if vals.get('state') == 'confirm':
            self.message_post(body="Prescription Confirmed")
        return res

    def action_print(self):
        template_id = self.env.ref('bista_hms.action_prescription_reprot')
        return template_id.report_action(self)

    def action_confirm(self):
        self.state = 'confirm'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['date'] = fields.Date.context_today(self)
        res['patient_id'] = self._context.get('patient_id')
        return res

    def action_create_delivery(self):
        """ stock.picking
            stock.move
            """

        picking_vals = self.prepare_picking_vals()

        picking_id = self.env['stock.picking'].create(picking_vals)

        move_vals = self.prepare_move_vals(picking_id)

        move_ids = self.env['stock.move'].create(move_vals)
        print("picking_id==========", picking_id)

        picking_id.action_confirm()

        # partner_id = picking_id.read(['partner_id'])
        # partner_id = partner_id[0]['partner_id'][0]
        picking_id.action_assign()
        # picking_id.button_validate()
        self.picking_ids = [(4, picking_id.id)]

    def prepare_picking_vals(self):
        picking_type_id = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
        vals = {
            'partner_id': 7,
            'picking_type_id': picking_type_id.id,
            'location_id': picking_type_id.default_location_src_id.id,
            'location_dest_id': picking_type_id.default_location_dest_id.id,
            # 'origin': self.name,
        }
        return vals

    def prepare_move_vals(self, picking_id):
        move_vals = []
        for line in self.prescription_lines:
            if line.move_ids:
                continue
            qty_in_move = sum(line.move_ids.mapped('product_uom_qty'))
            to_deliver = line.quantity - qty_in_move
            vals = {
                'picking_type_id': picking_id.picking_type_id.id,
                'location_id': picking_id.location_id.id,
                'location_dest_id': picking_id.location_dest_id.id,
                'picking_id': picking_id.id,
                'product_id': line.product_id.id,
                'name': line.product_id.display_name,
                'product_uom_qty': to_deliver,
                'prescription_line_id': line.id,
            }
            move_vals.append(vals)
        return move_vals

    @api.depends('prescription_lines.total')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.prescription_lines.mapped('total'))

    def action_create_invoice(self):
        if not self.prescription_lines:
            raise ValidationError("Please add prescription lines before creating an invoice.")
        # if not self.state == 'confirm':
        #     raise ValidationError("Prescription must be confirmed before creating an invoice.")

        vals = self.prepare_invoice_vals()
        # invoice_id = self.env['account.move'].create(vals)

        # vals['invoice_line_ids'] = line_vals

        invoice_id = self.env['account.move'].create(vals)

        line_vals_list = self.prepare_invoice_line_vals(invoice_id)

        line_ids  = self.env['account.move.line'].create(line_vals_list)

        self.invoice_ids = [(6, 0 , [invoice_id.id])]

        # self.invoice_ids = [(3, 25)]
        print("move_line_ids==========",invoice_id)


    def prepare_invoice_vals(self):
        values = {
            'move_type': 'out_invoice',
            'partner_id': 7, # self.patient_id.partner_id.id,
            'partner_shipping_id': 7, # # self.patient_id.partner_id.id,
            'company_id': self.env.user.company_id.id,
            'user_id': self.env.user.id,
            'invoice_date': self.date,
        }
        return values

    def prepare_invoice_line_vals(self, invoice_id):
        line_vals_list = []
        for line in self.prescription_lines:
            line_vals = {
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
                'discount': 0.0,
                'move_id': invoice_id.id,
            }
            line_vals_list.append(line_vals)
            # line_vals_list.append((0, 0, line_vals))
        return line_vals_list

class PrescriptionLine(models.Model):
    _name = "prescription.line"

    prescription_id = fields.Many2one("hms.prescription", string="Prescription", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Medicine", required=True)
    quantity = fields.Integer(string="Quantity", required=True)
    price_unit = fields.Float(string="Price Unit", required=True)
    total = fields.Float(string="Total", compute="_compute_total", store=True)
    move_ids = fields.One2many("stock.move", "prescription_line_id", string="Stock Moves")

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.price_unit = self.product_id.lst_price

    @api.depends('quantity', 'price_unit')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.price_unit

    @api.constrains('quantity')
    def check_quantity(self):
        for rec in self:
           qty_in_move = sum(rec.move_ids.mapped('product_uom_qty'))
           if rec.quantity < qty_in_move:
                raise ValidationError("Quantity in prescription cannot be less than quantity in stock move.")