from odoo import models, fields,api
from odoo.exceptions import ValidationError

class RMAInvoiceWizard(models.TransientModel):
    _name = 'rma.invoice.wizard'
    _description = 'RMA Processing Wizard'

    act_id = fields.Many2one('sale.rma',string="Default_id")
    line_ids = fields.One2many("rma.invoice.wizard.line",'rma_invoice_wizard_id')
    
   
    @api.onchange('act_id')
    def onchange_sale_order(self):
        if self.act_id:
            rma_lines = []
            for line in self.act_id.line_ids:
                    rma_lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'so_qty': line.so_qty,
                        'rma_line_id': line.id,
                        'to_invoiced': line.qty_to_invoice
                    }))
            self.line_ids = rma_lines
            
    def process_invoice(self):
        if not self.act_id:
            raise ValidationError("RMA record not found.")
        for wizard_line in self.line_ids:
            if wizard_line.to_invoiced <= 0:
                continue
            if wizard_line.to_invoiced > wizard_line.rma_line_id.qty_to_invoice:
                raise ValidationError(f"Invoice Quantity must be less than or equal to Qauntity to invoice for product {wizard_line.product_id.display_name} i.e. {wizard_line.rma_line_id.qty_to_invoice} ")
        self.action_create_invoice()
        #self.action_create_invoice()

    
    def action_create_invoice(self):
        if not self.line_ids:
            raise ValidationError("Please add lines before creating an invoice.")
        vals = self.prepare_invoice_vals()
        invoice_id = self.env['account.move'].create(vals)
        line_vals_list = self.prepare_invoice_line_vals(invoice_id)
        line_ids = self.env['account.move.line'].create(line_vals_list)
        self.act_id.invoice_ids = [(4,(invoice_id.id))]

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
            if line.to_invoiced <= 0:
                continue
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
