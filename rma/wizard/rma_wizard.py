from odoo import models, fields,api
from odoo.exceptions import ValidationError

class RMAWizard(models.TransientModel):
    _name = 'rma.wizard'
    _description = 'RMA Processing Wizard'

    act_id = fields.Integer(string="Default_id")
    line_ids = fields.One2many("rma.wizard.line",'rma_wizard_id')
   

    def process(self):
        rma_record_id = self.act_id
        rma_record = self.env['sale.rma'].browse(rma_record_id)
        if not rma_record_id:
            raise ValidationError("RMA record not found.")
        for wizard_line in self.line_ids:
            if wizard_line.return_qty <= 0:
                continue
            if wizard_line.so_qty < wizard_line.return_qty:
                raise ValidationError(f"Return Quantity must be less than sale Qty i.e. {wizard_line.so_qty}")
            
            rma_line = self.env['sale.rma.line'].search([('rma_id', '=', rma_record_id),
                                                         ('product_id', '=', wizard_line.product_id.id)], limit=1)
            if not rma_line:
                raise ValidationError(f"No matching RMA line found for product {wizard_line.product_id.display_name}.")
            remaining_qty = rma_line.to_receive - wizard_line.return_qty
        
            rma_line.returned_qty += wizard_line.return_qty
            rma_line.to_receive = remaining_qty
            rma_line.received_qty = remaining_qty
        rma_record.action_create_delivery()
            
    def default_get(self, fields_list):
        res = super(RMAWizard, self).default_get(fields_list)
        res['act_id'] = self.env.context.get('active_id')
        return res

    @api.onchange('act_id')
    def onchange_sale_order(self):
        if self.act_id:
            records = self.env['sale.rma'].browse(self.act_id)
            rma_lines = []
            rma_lines = [(5, 0, 0)]
            for line in records.line_ids:
                rma_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'so_qty': line.to_receive,
                }))
            self.update({'line_ids': rma_lines})
