from odoo import fields, models, api
from  dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError


class HotelResrvationHistory(models.Model):
    _name = 'hotel.reservation.history'
    _description = 'Hotel Resrevation History'

    name = fields.Many2one('hotel.reservation', string="Booking Id")
    guest_id = fields.Many2one('hotel.guest', string='Guest Name')
    room_id = fields.Many2one('hotel.room', string="Room No")
    booking_date = fields.Date(string='Booking Date', required=True, default=fields.Datetime.now())
    check_in_time = fields.Datetime(string='Check In', default=fields.Datetime.now())
    check_out_time = fields.Datetime(string='Check Out')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('booked','Booked'),
        ('check_in','Check In'),
        ('check_out','Check Out'),
        ('canceled', "Cancelled")
    ],default='draft',string='Status')
    amount_total = fields.Float(string="Amount Total", compute="_copute_total", store=True)

