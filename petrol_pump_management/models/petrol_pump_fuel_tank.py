from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PetrolPumpFuelTank(models.Model):
    _name = 'petrol.pump.fuel.tank'
    _description = 'Fuel Tank'
    _rec_name = 'fuel_type'
    
    station_id = fields.Many2one('petrol.pump.station', string='Station', required=True)
    fuel_type = fields.Selection([
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('cng', 'CNG')
    ], string='Fuel Type', required=True)
    capacity = fields.Float(string='Tank Capacity (Liters)', required=True)
    current_stock = fields.Float(string='Current Stock (Liters)', compute='_compute_current_stock', store=True)

    @api.constrains('capacity')
    def _check_capacity(self):
        for rec in self:
            if rec.capacity <= 0:
                raise ValidationError('Tank capacity must be greater than zero.')

    @api.constrains('fuel_type')
    def _check_fuel_type_unique(self):
        for rec in self:
            domain = [('station_id', '=', rec.station_id.id), ('fuel_type', '=', rec.fuel_type), ('id', '!=', rec.id)]
            if self.search_count(domain):
                raise ValidationError('Each fuel type must be unique per station.')

    def action_replenish_tank(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Replenish Tank',
            'res_model': 'petrol.pump.replenish.tank.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_tank_id': self.id}
        }

    def replenish_stock(self, quantity):
        if quantity <= 0:
            raise ValidationError('Quantity must be greater than zero.')
        if self.current_stock + quantity > self.capacity:
            raise ValidationError('Cannot exceed tank capacity.')
        self.current_stock += quantity

    def _compute_current_stock(self):
        for rec in self:
            sales = self.env['petrol.pump.sale.line'].search([('dispenser_id.tank_id', '=', rec.id)])
            total_sold = sum(sales.mapped('quantity'))
            rec.current_stock = rec.capacity - total_sold
            
    @api.model
    def cron_check_low_stock(self):
        tanks = self.search([])
        for tank in tanks:
            if tank.capacity > 0 and tank.current_stock < (0.1 * tank.capacity):
                if tank.station_id.manager_id.email:
                    template = self.env.ref('petrol_pump_management.low_stock_email_template')
                    template.send_mail(tank.id, force_send=True)

