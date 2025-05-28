from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError

class HotelGuests(models.Model):
    _name = 'hotel.guest'
    _description = 'Guest Information'

    guest_id = fields.Char(string='Guest ID', copy=False, readonly=True, default="New")
    name = fields.Many2one('res.partner', copy=False, string='Name', required=True)
    phone = fields.Char(string='Phone', copy=False, required=True)
    email = fields.Char(string='Email', copy=False)
    id_proof = fields.Char(string="ID Proof", copy=False)
    nationality = fields.Char(string="Nationality", default="Indian")
    stay_history_ids = fields.One2many('hotel.reservation', 'guest_id', copy=False, string="Stay History")

    @api.model_create_multi
    def create(self, vals_list):
        template_id = self.env.ref('hotel_management.email_template_register_user')
        for vals in vals_list:
            if vals.get('guest_id', 'New') == 'New':
                vals['guest_id'] = self.env['ir.sequence'].next_by_code('hotel.guest') or '/'
            if vals.get('email'):
                if template_id:
                    template_id.send_mail(self.id, force_send=True)
                else:
                    raise UserError("Mail Template not found. Please check the template.")
        return super(HotelGuests, self).create(vals_list)

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            if self.name.phone:
                self.phone = self.name.phone
            if self.name.email:
                self.email = self.name.email
    
    @api.constrains('phone')
    def _check_phone(self):
        for rec in self:
            if rec.phone:
                if not rec.phone.isdigit():
                    raise ValidationError("Phone number must contain only digits.")
                if len(rec.phone) != 10:
                    raise ValidationError("Phone number must be exactly 10 digits.")
                existing = self.search([('phone', '=', rec.phone),('id', '!=', rec.id)])
                if existing:
                    raise ValidationError("This phone number is already used by another guest.")

