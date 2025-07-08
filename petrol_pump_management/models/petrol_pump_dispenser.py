from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PetrolPumpDispenser(models.Model):
    _name = 'petrol.pump.dispenser'
    _description = 'Fuel Dispenser'
    _rec_name = 'code'
    
    station_id = fields.Many2one('petrol.pump.station', string='Station', required=True)
    tank_id = fields.Many2one(
        'petrol.pump.fuel.tank',
        string='Connected Tank',
        required=True,
        domain="[('station_id', '=', station_id)]"
    )
    code = fields.Char(string='Dispenser Code', copy="False", required=True)
    operator_id = fields.Many2one('res.users', string='Assigned Operator', required=True)
    sales_line_ids = fields.One2many('petrol.pump.sale.line', 'dispenser_id', string='Sales Lines')

    @api.constrains('code')
    def _check_code_unique_per_station(self):
        for rec in self:
            domain = [('station_id', '=', rec.station_id.id), ('code', '=', rec.code), ('id', '!=', rec.id)]
            if self.search_count(domain):
                raise ValidationError('Dispenser code must be unique per station.')

    @api.constrains('tank_id')
    def _check_tank_station_match(self):
        for rec in self:
            if rec.station_id and rec.tank_id.station_id and rec.station_id != rec.tank_id.station_id:
                raise ValidationError('Dispenser station must match tank station.')
            
    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        group = self.env.ref('petrol_pump_management.group_pump_operator')
        self = self.with_context(operator_domain=[('groups_id', 'in', [group.id])])
        return res