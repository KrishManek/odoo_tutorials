from odoo import fields, models, api
from odoo.exceptions import ValidationError

class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'

    name = fields.Char(string="Room Name", copy=False, default="New", readonly=True)
    category_id = fields.Many2one('hotel.room.category', string="Room Category", required=True)
    price_per_night = fields.Float("Room Rent", compute='_compute_price', readonly=False, store=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved')
    ], default='available', required=True)
    is_available = fields.Boolean("Is Available", compute="_compute_availability", store=True)
    current_guest_id = fields.Many2one('hotel.guest', string="Current Guest", compute='_compute_current_guest', store=True)
    booking_history_ids = fields.One2many('hotel.reservation.history', 'room_id', copy=False, string="Booking History")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('hotel.room') or '/'
        return super().create(vals_list)

    @api.depends('category_id')
    def _compute_price(self):
        for room in self:
            room.price_per_night = room.category_id.price if room.category_id else 0.0

    @api.depends('status', 'current_guest_id')
    def _compute_availability(self):
        for room in self:
            room.is_available = room.status == 'available' and not room.current_guest_id

    @api.depends('status')
    def _compute_current_guest(self):
        for room in self:
            if room.status != 'occupied':
                room.current_guest_id = False

    @api.constrains('price_per_night')
    def _check_price_positive(self):
        for room in self:
            if room.price_per_night < 0:
                raise ValidationError("Room rent cannot be negative.")
            
    @api.constrains('status', 'current_guest_id')
    def _check_guest_and_status(self):
        for room in self:
            if room.status == 'available' and room.current_guest_id:
                raise ValidationError("Available rooms should not have a guest assigned.")
            if room.status == 'occupied' and not room.current_guest_id:
                raise ValidationError("Occupied rooms must have a guest assigned.")
