from odoo import models, fields,api
from odoo.exceptions import UserError

class AssignSerial(models.TransientModel):
    _name = 'assign.serial'
    _description = 'Sale Add Product Wizard'

    mrp_id = fields.Many2one('mrp.production',string="Default_id")
    no_seq = fields.Integer(string="No Of Sequnece to Generate")
    gen_seq = fields.Integer(string="Generated seq", compute="_calculate_gen_seq", store=True)
    
    @api.onchange('mrp_id')
    def _onchange_mrp_id(self):
        self.no_seq = self.mrp_id.product_qty - self.gen_seq

    @api.depends('mrp_id.serial_ids','mrp_id.product_id')
    def _calculate_gen_seq(self):
        for rec in self:
            self.gen_seq = len(rec.mrp_id.serial_ids)
        
    def generate_seq(self):        
        seq = self.mrp_id.product_id.sequence_id
        if (self.no_seq + self.mrp_id.product_qty) >= self.gen_seq and self.no_seq < 0:
            raise UserError(f"Please Enter Valid Quantity")
        serial_nos = []
        for quantity in range(self.no_seq):
            serial_no = seq.next_by_id()
            serial_nos.append((0,0,{'name':serial_no,
                                   'product_id':self.mrp_id.product_id.id}))
        self.mrp_id.serial_ids = serial_nos
        
    