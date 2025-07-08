from odoo import models, fields, api
from odoo.exceptions import UserError

class DispenserDashboardWizard(models.TransientModel):
    _name = 'petrol.pump.dispenser.dashboard.wizard'
    _description = 'Dispenser Dashboard Wizard'

    station_ids = fields.Many2many('petrol.pump.station', string='Station')
    dispenser_ids = fields.Many2many('petrol.pump.dispenser', string='Dispenser', readonly=False, compute='_compute_dispenser_ids', store=False)
    fuel_type = fields.Selection([
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('cng', 'CNG'),
    ], string='Fuel Type')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To', default=fields.Date.today())
    current_stock = fields.Float(string='Current Stock', compute='_compute_current_stock', store=False)
    total_sold = fields.Float(string='Total Sold', compute='_compute_total_sold', store=False)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=False)
    result_ids = fields.One2many('petrol.pump.dispenser.dashboard.line', 'wizard_id', string='Results')

    def compute_all(self):
        self.station_ids = self._get_compute_station_ids()
        self._compute_dispenser_ids()
        self._compute_total_sold()
        self._compute_current_stock()
        self._compute_total_amount()

    def _compute_total_amount(self):
        for rec in self:
            if rec.dispenser_ids and rec.dispenser_ids.sales_line_ids:
                total_amount = sum(
                    line.total_amount
                    for line in rec.dispenser_ids.mapped('sales_line_ids')
                    if line.date and (
                        (not rec.date_from or line.date.date() >= rec.date_from)
                        and (not rec.date_to or line.date.date() <= rec.date_to)
                    )
                )
                rec.total_amount = total_amount
            else:
                rec.total_amount = 0.0

    def _get_compute_station_ids(self):
        if self.station_ids:
            return [station.id for station in self.station_ids]
        return self.env['petrol.pump.station'].search([]).ids
        
    def _compute_dispenser_ids(self):
        for rec in self:
            if rec.station_ids:
                rec.dispenser_ids = rec.station_ids.mapped('dispenser_ids')
            else:
                rec.dispenser_ids = self.env['petrol.pump.dispenser']

    def _compute_total_sold(self):
        for rec in self:
            if rec.station_ids:
                total_sold = sum(
                    line.quantity for line in rec.station_ids.mapped('dispenser_ids.sales_line_ids')
                    if (not rec.date_from or line.date.date() >= rec.date_from) and (not rec.date_to or line.date.date() <= rec.date_to)
                )
                rec.total_sold = total_sold
            else:
                rec.total_sold = 0.0
                
    def _compute_current_stock(self):
        for rec in self:
            if rec.station_ids:
                total_stock = sum(tank.current_stock for station in rec.station_ids for tank in station.fuel_tank_ids)
                rec.current_stock = total_stock
            else:
                rec.current_stock = 0.0 
                
    def action_generate_report(self):
        # Clear old lines
        self.result_ids.unlink()

        domain = []
        if self.station_ids:
            domain += [('station_id', 'in', self.station_ids.ids)]
        if self.fuel_type:
            domain += [('tank_id.fuel_type', '=', self.fuel_type)]

        dispensers = self.env['petrol.pump.dispenser'].search(domain)
        today = fields.Date.today()

        lines = []
        for dispenser in dispensers:
            total_sold = sum(
                l.quantity for l in dispenser.sales_line_ids
                if (not self.date_from or l.date.date() >= self.date_from) and
                   (not self.date_to or l.date.date() <= self.date_to)
            )
            date = dispenser.sales_line_ids and dispenser.sales_line_ids[0].date or today
            lines.append((0, 0, {
                'date': date,
                'station_id': dispenser.station_id.id,
                'dispenser_id': dispenser.id,
                'tank_id': dispenser.tank_id.id,
                'current_stock': dispenser.tank_id.current_stock,
                'total_sold': total_sold,
            }))
        self.result_ids = lines
        if not self.result_ids:
            raise UserError("No results found for the selected criteria.")
        self.compute_all()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'petrol.pump.dispenser.dashboard.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def action_download_pdf(self):
        if not self.result_ids:
            raise UserError("Nothing to download")
        return self.env.ref('petrol_pump_management.report_dispenser_dashboard').report_action(self)
