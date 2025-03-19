from odoo import fields, models, api
from odoo.exceptions import ValidationError

# Define the HospitalDetails model
class HospitalDetails(models.Model):
    _name = "hospital.details"  # Model name
    _description = "Hospital Details"  # Model description

    # Define fields for the model
    name = fields.Char(string="Hospital Name", required=True)  # Hospital name
    address = fields.Char(string="Address")  # Hospital address
    phone = fields.Char(string="Phone Number")  # Hospital phone number
    email = fields.Char(string="Email")  # Hospital email
    is_public = fields.Boolean(string="Public Hospital", default=True)  # Public hospital flag
    doctor_ids = fields.One2many('res.doctor', 'hospital_id', string="Doctors")  # One-to-many relation to doctors