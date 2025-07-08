from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PetrolPumpSaleLine(models.Model):
    _name = 'petrol.pump.sale.line'
    _description = 'Fuel Sale Line'
    _rec_name = 'dispenser_id'
    
    dispenser_id = fields.Many2one('petrol.pump.dispenser', string='Dispenser', required=True)
    date = fields.Datetime(string='Sale Date', default=fields.Datetime.now)
    quantity = fields.Float(string='Quantity Sold (Liters)', required=True)
    unit_price = fields.Float(string='Unit Price', required=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    customer_id = fields.Many2one('res.partner', string='Customer')
    
    @api.constrains('quantity', 'unit_price')
    def _check_positive_values(self):
        for rec in self:
            if rec.quantity <= 0 or rec.unit_price <= 0:
                raise ValidationError('Quantity and unit price must be greater than zero.')

    @api.depends('quantity', 'unit_price')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.quantity * rec.unit_price

    @api.model
    def create(self, vals):
        sale = super().create(vals)
        tank = sale.dispenser_id.tank_id
        if sale.quantity > tank.current_stock:
            raise ValidationError('Not enough fuel in the tank.')
        tank.current_stock -= sale.quantity
        sale.create_invoice()
        return sale

    def create_invoice(self):
        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': "fleet" if not self.customer_id else self.customer_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': self.dispenser_id.tank_id.fuel_type,
                'quantity': self.quantity,
                'price_unit': self.unit_price,
            })]
        })
        move.action_post()
        return move
