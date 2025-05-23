from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


# Define the HmsPrescription model
class HmsPrescription(models.Model):
    _name = "hms.prescription"  # Model name
    _description = "Prescription"  # Model description
    _res_name = "patient_id"  # Field used for record name

    # Define fields for the model
    prescription_code = fields.Char(string="Id", required=True, default="New")  # Prescription code
    patient_id = fields.Many2one('patient.details', string="Patient", required=True)  # Reference to patient details
    date = fields.Date(string="Date", default=fields.Date.today, required=True)  # Prescription date
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')], string="Status", default='draft', required=True)  # Prescription state
    prescription_lines = fields.One2many('hms.prescription.line', 'prescription_id', string="Prescription Lines")  # One-to-many relation to prescription lines
    prescription_count = fields.Integer(compute="_compute_prescription_count", string="Prescription Count", store=True)  # Computed field for prescription count
    total = fields.Integer(string='Total', compute="_compute_prescription_total", store=True)  # Computed field for total amount
    invoice_ids = fields.Many2many("account.move", string="Invoices")
    #picking_ids = fields.Many2many("stock.picking", string="Invoices")
    picking_ids = fields.One2many("stock.picking", 'prescription_id', string="Prescription")
    delivery_count = fields.Integer(compute="_compute_delivery_count", string="Delivery Count", store=True)
    #delivered_qty = fields.Integer(string="Delivered Quantity", compute='_compute_delivered_qty', store=True)
    #remaining_qty = fields.Integer(string="Remaining  Quantity")
    #move_ids = fields.One2many("stock.move", 'prescription_id', string="Prescription")
    
    # delivery_count = fields.Integer(compute="_compute_picking_ids", string="Delivery Count", store=True)


    # Override the create method to generate a unique prescription code
    @api.model_create_multi
    def create(self, vals_list):
        res = super(HmsPrescription, self).create(vals_list)
        for result in res:
            result.prescription_code = self.env['ir.sequence'].next_by_code('hms.prescription')
        return res
    
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['date'] = fields.Date.context_today(self)
        res['patient_id'] = self._context.get('patient_id')
        return res
    
    # Compute the total amount of the prescription
    @api.depends('prescription_lines.sub_total')
    def _compute_prescription_total(self):
        for rec in self:
            rec.total = sum(rec.prescription_lines.mapped('sub_total'))

    # Compute the count of prescription lines
    @api.depends('prescription_lines')
    def _compute_prescription_count(self):
        for patient in self:
            patient.total = self.env['hms.prescription.line'].search_count([('prescription_id', '=', patient.id)])

    @api.depends('picking_ids')
    def _compute_delivery_count(self):
        for delivery in self:
            delivery.delivery_count = self.env['stock.picking'].search_count([('prescription_id', '=', delivery.id)])
   
    # Action to confirm the prescription
    def action_confirm_prescription(self):
        self.state = 'confirmed'

    # Action to cancel the prescription
    def action_cancel_prescription(self):
        self.state = 'canceled'

    # Action to open the prescription lines
    def action_open_prescriptions(self):
        form_view_id = self.env.ref('hms.view_hms_prescription_line_form').id  # Get form view ID
        list_view_id = self.env.ref('hms.view_hms_prescription_line_list').id  # Get list view ID

        res = {
            'name': 'Prescriptions',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hms.prescription.line',
            'view_id': form_view_id,
            'target': 'current',
            'context': {'default_patient_id': self.id}
        }
        if self.prescription_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('prescription_id', '=', self.id)]
            res['view_id'] = False
        return res
    
    def action_open_delivery(self):
        form_view_id = self.env.ref('stock.view_picking_form').id  # Get form view ID
        list_view_id = self.env.ref('stock.vpicktree').id  # Get list view ID

        res = {
            'name': 'Stock Picking',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'target': 'current',
            'domain': [('prescription_id', '=', self.id)],
            'views':[(list_view_id, 'list'), (form_view_id, 'form')],
            'view_mode': 'list,form'   
        }

        return res

    def action_create_invoice(self):
        if not self.prescription_lines:
            raise ValidationError("Please add prescription lines before creating an invoice.")
        vals = self.prepare_invoice_vals()
        invoice_id = self.env['account.move'].create(vals)
        line_vals_list = self.prepare_invoice_line_vals(invoice_id)
        line_ids = self.env['account.move.line'].create(line_vals_list)
        self.invoice_ids = [(6,0,[invoice_id.id])]

    def prepare_invoice_vals(self):
        values = {
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.partner_id.id,  
            'partner_shipping_id': self.patient_id.partner_id.id,
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
                'quantity': line.qty,
                'price_unit': line.price_unit,
                'discount': 0.0,
                'move_id': invoice_id.id,
            }
            line_vals_list.append(line_vals)
            # line_vals_list.append((0, 0, line_vals))
        return line_vals_list
    
    def action_create_delivery(self):
        picking_vals = self.prepare_picking_vals()
        picking_id = self.env['stock.picking'].create(picking_vals)
        move_vals = self.prepare_move_vals(picking_id)
        move_id = self.env['stock.move'].create(move_vals)
        picking_id.action_confirm()
        picking_id.action_assign()
        #picking_id.button_validate()

    def prepare_picking_vals(self):
        picking_type_id = self.env['stock.picking.type'].search([('code', '=','outgoing')], limit=1)
        vals = {
            'partner_id' : self.patient_id.partner_id.id,
            'picking_type_id' : picking_type_id.id,
            'location_id' : picking_type_id.default_location_src_id.id,
            'location_dest_id' : picking_type_id.default_location_dest_id.id,
            'origin': self.prescription_code,
            'prescription_id' : self.id

        }
        return vals
    def prepare_move_vals(self, picking_id):
        move_vals=[]
        for line in self.prescription_lines:
            qty_in_move = sum(line.move_ids.mapped('product_uom_qty'))
            to_deliver = line.qty - qty_in_move
            if to_deliver == 0:
                continue
            vals = {
                    'picking_type_id' : picking_id.picking_type_id.id,
                    'location_id' : picking_id.location_id.id,
                    'location_dest_id' : picking_id.location_dest_id.id,
                    'picking_id' : picking_id.id,
                    'product_id' : line.product_id.id,
                    'product_uom_qty': to_deliver,
                    'name' : line.product_id.display_name,
                    'prescription_line_id':line.id
                }
            move_vals.append(vals)
        return move_vals
    