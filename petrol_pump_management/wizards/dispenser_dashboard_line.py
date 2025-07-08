from odoo import models, fields

class DispenserDashboardLine(models.TransientModel):
    _name = 'petrol.pump.dispenser.dashboard.line'
    _description = 'Dispenser Dashboard Line'

    wizard_id = fields.Many2one('petrol.pump.dispenser.dashboard.wizard')
    station_id = fields.Many2one('petrol.pump.station', string='Station')
    dispenser_id = fields.Many2one('petrol.pump.dispenser', string='Dispenser')
    tank_id = fields.Many2one('petrol.pump.fuel.tank', string='Tank')
    current_stock = fields.Float(string='Current Stock')
    total_sold = fields.Float(string='Total Sold')
    date = fields.Datetime(string='Sale Date', default=fields.Datetime.now)
