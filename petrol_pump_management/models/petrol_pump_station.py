from odoo import models, fields

class PetrolPumpStation(models.Model):
    _name = 'petrol.pump.station'
    _description = 'Petrol Pump Station'

    name = fields.Char(string='Station Name', required=True)
    location = fields.Char(string='Location', required=True)
    manager_id = fields.Many2one('res.partner', string='Station Manager', required=True, domain="[('is_company', '=', False)]")
    fuel_tank_ids = fields.One2many('petrol.pump.fuel.tank', 'station_id', string='Fuel Tanks')
    dispenser_ids = fields.One2many('petrol.pump.dispenser', 'station_id', string='Dispensers')
