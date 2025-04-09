from odoo import api,fields,models

class Product(models.Model):
    _inherit = 'product.template'

    def action_open_upd_wizard(self):
        veiw_id = self.env.ref("hms.update_onhand_quantity_wizard").id
        return {
            'name' : "Quantity",
            'view_mode' : "form",
            'res_model' : 'update.qty.available',
            'view_id' : veiw_id,
            'type' : "ir.actions.act_window",
            'target' : 'new',
        }

