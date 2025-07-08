from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ReplenishTankWizard(models.TransientModel):
    _name = 'petrol.pump.replenish.tank.wizard'
    _description = 'Replenish Tank Wizard'

    tank_id = fields.Many2one('petrol.pump.fuel.tank', string='Tank', required=True)
    quantity = fields.Float(string='Replenish Quantity (Liters)', required=True)

    def action_replenish(self):
        self.ensure_one()
        if self.quantity <= 0:
            raise ValidationError('Quantity must be greater than zero.')
        self.tank_id.replenish_stock(self.quantity)
