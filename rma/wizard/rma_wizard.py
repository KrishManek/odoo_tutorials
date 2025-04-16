from odoo import models, fields,api
from odoo.exceptions import ValidationError

class RMAWizard(models.TransientModel):
    _name = 'rma.wizard'
    _description = 'RMA Processing Wizard'

    act_id = fields.Many2one('sale.rma',string="Default_id")
    line_ids = fields.One2many("rma.wizard.line",'rma_wizard_id')
    
   
    @api.onchange('act_id')
    def onchange_sale_order(self):
        if self.act_id:
            rma_lines = []
            for line in self.act_id.line_ids:
                if line.so_qty > line.received_qty:
                    rma_lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'so_qty': line.so_qty,
                        'return_qty': line.so_qty - line.to_receive,
                        'rma_line_id': line.id,
                    }))
            self.line_ids = rma_lines
            
    def process(self):
        if not self.act_id:
            raise ValidationError("RMA record not found.")
        for wizard_line in self.line_ids:
            if wizard_line.return_qty <= 0:
                continue
            if wizard_line.return_qty > wizard_line.rma_line_id.so_qty - wizard_line.rma_line_id.to_receive:
                raise ValidationError(f"Return Quantity must be less than or equal torecive Qty for product {wizard_line.product_id.display_name}.")

            """ rma_line = self.env['sale.rma.line'].search([
                                                ('rma_id', '=', self.act_id.id),
                                                ('product_id', '=', wizard_line.product_id.id)
                                                ], limit=1)
            if not rma_line:
                raise ValidationError(f"No matching RMA line found for product {wizard_line.product_id.display_name}.")
            # Update RMA line
            rma_line.received_qty += wizard_line.return_qty
            rma_line.returned_qty += wizard_line.return_qty """
        self.action_create_delivery()
        """ self.act_id.line_ids._compute_qty()
        self.act_id.line_ids._compute_invoice_qty()
        self.line_ids._compute_inv_qty() """
        #self.action_create_invoice()


    def action_create_delivery(self):
        picking_vals = self.prepare_picking_vals()
        picking = self.env['stock.picking'].create(picking_vals)
        move_vals = self.prepare_move_vals(picking)
        if not move_vals:
            picking.unlink()
            raise ValidationError("No valid return quantities to deliver.")
        moves = self.env['stock.move'].create(move_vals)
        """ picking._action_confirm(merge=True)
        picking._action_assign() """
        
        old_draft_moves = picking.move_ids.filtered(lambda m: m.state == 'draft' and m not in moves)
        if old_draft_moves:
            old_draft_moves._action_confirm(merge=False)

        moves._action_confirm(merge=False)
        #picking.action_assign()
        # Optional:
        # picking.button_validate()

    def prepare_picking_vals(self):
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
        if not picking_type:
            raise ValidationError("No incoming picking type found.")
        return {
            'partner_id': self.act_id.sale_order_id.partner_id.id,
            'picking_type_id': picking_type.id,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id,
            'origin': self.act_id.name,
            'rma_id': self.act_id.id,
        }

    def prepare_move_vals(self, picking):
        move_vals = []
        for line in self.line_ids:
            if line.return_qty <= 0:
                continue

            move_vals.append({
                'picking_id': picking.id,
                'product_id': line.product_id.id,
                #'product_uom': line.product_id.uom_id.id,
                'product_uom_qty': line.return_qty,
                'name': line.product_id.display_name,
                'picking_type_id': picking.picking_type_id.id,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
                'rma_line_id': line.rma_line_id.id,
            })
        return move_vals
    
    """ def action_create_invoice(self):
        if not self.line_ids:
            raise ValidationError("Please add lines before creating an invoice.")
        vals = self.prepare_invoice_vals()
        invoice_id = self.env['account.move'].create(vals)
        line_vals_list = self.prepare_invoice_line_vals(invoice_id)
        line_ids = self.env['account.move.line'].create(line_vals_list)
        self.act_id.invoice_ids = [(6,0,[invoice_id.id])]

    def prepare_invoice_vals(self):
        values = {
            'move_type': 'out_invoice',
            'partner_id': self.act_id.sale_order_id.partner_id.id,  
            'partner_shipping_id': self.act_id.sale_order_id.partner_id.id,
            'company_id': self.env.user.company_id.id,
            'user_id': self.env.user.id,
            'invoice_date': fields.date.today(),
            'rma_id': self.act_id.id,
        }
        return values
    
    def prepare_invoice_line_vals(self, invoice_id):
        line_vals_list = []
        for line in self.line_ids:
            
            line_vals = {
                'product_id': line.product_id.id,
                'quantity': line.to_invoiced,
                'price_unit': line.rma_line_id.unit_price,
                'discount': 0.0,
                'move_id': invoice_id.id,
                'rma_line_id': line.rma_line_id.id,
            }
            line_vals_list.append(line_vals)
            # line_vals_list.append((0, 0, line_vals))
        return line_vals_list
 """