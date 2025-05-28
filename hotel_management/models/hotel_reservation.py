from odoo import fields, models, api
from  dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError


class HotelResrvation(models.Model):
    _name = 'hotel.reservation'
    _description = 'Hotel Resrevation'

    name = fields.Char(string='Reservation ID',copy=False, readonly=True, default="New")
    guest_id = fields.Many2one('hotel.guest', string='Guest Name')
    room_category = fields.Many2one('hotel.room.category', string="Room Category")
    room_ids = fields.Many2many('hotel.room', string="Room No", domain="[('status', '=', 'available'), ('category_id', '=', room_category)]" )
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
    rent = fields.Float(string="Room Rent")
    amount_total = fields.Float(string="Amount Total", compute="_copute_total", store=True)
    amount_paid = fields.Float(string="Amount Paid")
    amount_remaining = fields.Float(string="Amount Remaining", compute="_compute_amount_remaining", store=True)
    payment_status = fields.Selection([
        ('not_paid','Not Paid'),
        ('full_paid', "Full Payment"),
        ('partial','Partial Paid')
    ], default='not_paid', compute='_compute_payment_status', store=True, string="Payment Status")
    
    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True)


    @api.model_create_multi
    def create(self,vals_list):
        res = super(HotelResrvation,self).create(vals_list)
        for rec in res:
            rec.name = self.env['ir.sequence'].next_by_code('hotel.reservation')
        return res
    
    @api.onchange('room_ids')
    def _onchange_rooms(self):
        for rec in self.room_ids:
            if rec:
                self.rent = rec.price_per_night

    @api.depends('amount_total', 'amount_paid')
    def _compute_amount_remaining(self):
        for rec in self:
            rec.amount_remaining = max(rec.amount_total - rec.amount_paid, 0)

    @api.depends('rent', 'check_out_time', 'check_in_time', 'room_ids')
    def _copute_total(self):
        for rec in self:
            no_of_days = 0
            if rec.check_out_time and rec.check_in_time:
                no_of_days = (rec.check_out_time.date() - rec.check_in_time.date()).days
                if no_of_days <= 0:
                    no_of_days = 1
            if rec.rent:
                rec.amount_total = rec.rent * len(rec.room_ids) * no_of_days
    
    @api.depends('amount_total', 'amount_paid', 'invoice_id.amount_residual')
    def _compute_payment_status(self):
        for rec in self:
            if rec.invoice_id.amount_residual > 0:
                rec.amount_paid = rec.amount_total - rec.invoice_id.amount_residual 
            else:
                rec.amount_paid = 0
            if rec.amount_paid == 0:
                rec.payment_status = 'not_paid'
            elif rec.amount_paid >= rec.amount_total:
                rec.payment_status = 'full_paid'
            else:
                rec.payment_status = 'partial'

    @api.constrains('check_out_time')
    def _check_dates(self):
        for rec in self: 
            if rec.check_out_time and rec.check_out_time < rec.check_in_time:
                raise ValidationError("Check-out time must be after check-in time. ")
            
    @api.constrains('check_in_time')
    def _validate_check_in_time(self):
        for rec in self:
            if rec.check_in_time < fields.Datetime.now():
                raise ValidationError("Check-out time must be booking date. ") 
            
    @api.constrains('amount_total', 'amount_paid')
    def _check_amounts(self):
        for rec in self:
            if rec.amount_total < 0:
                raise ValidationError("Total amount cannot be negative.")
            if rec.amount_paid < 0:
                raise ValidationError("Amount paid cannot be negative.")
            if rec.amount_paid > rec.amount_total:
                raise ValidationError("Amount paid cannot exceed total amount.")
            
    def action_book(self):
        for rec in self:
            unavailable_rooms = rec.room_ids.filtered(lambda room: room.status in ['occupied', 'reserved', 'maintenance'])
            if unavailable_rooms:
                raise UserError(
                    f"Cannot book. The following rooms are not available:\n" +
                    ', '.join(unavailable_rooms.mapped('name'))
                )
            rec.room_ids.write({'status': 'reserved'})
            rec.state = 'booked'
            template_id = self.env.ref('hotel_management.email_template_booking_registration')
            if template_id:
                if rec.guest_id.email:
                    template_id.send_mail(self.id, force_send=True)
            else:
                raise UserError("Mail Template not found. Please check the template.")
                   
    def action_cancel(self):
        for rec in self:
            rec.room_ids.write({'status': 'available'})
            rec.state = 'canceled'

    def action_check_out(self):
        for rec in self:
            rec.check_out_time = fields.Datetime.now()
            rec.room_ids.write({'status': 'available', 'current_guest_id': False})
            rec.state = 'check_out'
            if not rec.invoice_id:
                self.action_create_invoice()
            
    def action_check_in(self):
        for rec in self:
            rec.check_out_time = fields.Datetime.now()
            rec.room_ids.write({'status': 'available', 'current_guest_id': rec.guest_id.id})
            rec.state = 'check_in'
            for room in rec.room_ids:
                room.booking_history_ids.create({
                    'name' : rec.id,
                    'guest_id' : rec.guest_id.id,
                    'room_id' : room.id,
                    'booking_date' : rec.booking_date,
                    'check_in_time' : rec.check_in_time,
                    'check_out_time' : rec.check_out_time,
                    'state' : rec.state,
                    'amount_total' : rec.amount_total
                    
                })

    def action_create_invoice(self):
        for rec in self:
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': rec.guest_id.name.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [(0, 0, {
                    'name': f'Room Booking: {rec.name}',
                    'quantity': 1,
                    'price_unit': rec.amount_total,
                })]
            })
            rec.invoice_id = invoice.id
            invoice.action_post()            
