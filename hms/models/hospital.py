from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HospitalDetails(models.Model):
    _name = "hospital.details"
    _description = "Hospital Details"

    name = fields.Char(string="Hospital Name", required=True)
    address = fields.Char(string="Address")
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email")
    is_public = fields.Boolean(string="Public Hospital", default=True)
    doctor_ids = fields.One2many('res.doctor', 'hospital_id', string="Doctors")