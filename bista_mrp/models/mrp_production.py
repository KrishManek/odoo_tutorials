from odoo import fields, models,api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    serial_ids = fields.Many2many('stock.lot', string="Serial No.")
    
    def open_serial_wizard(self):
        veiw_id = self.env.ref("bista_mrp.view_assign_sequnece_wizard_form").id
        return {
            'name' : "Generate Sequence Window",
            'view_mode' : "form",
            'res_model' : 'assign.serial',
            'view_id' : veiw_id,
            'type' : "ir.actions.act_window",
            'target' : 'new',
            'context': {'default_mrp_id': self.id}
        }
                
    def _split_productions(self, amounts=False, cancel_remaining_qty=False, set_consumed_qty=False):
        res = super()._split_productions(amounts, cancel_remaining_qty, set_consumed_qty)
        res[-1].write({'serial_ids':[(3, res[0].lot_producing_id.id)]})
        res[0].write({'serial_ids':[(3, res[0].lot_producing_id.id)]})
        return res