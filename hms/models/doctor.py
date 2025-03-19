from odoo import fields, models, api
from odoo.exceptions import ValidationError


# Define the DoctorDetails model
class DoctorDetails(models.Model):
    _name = "res.doctor"  # Model name
    _description = "Doctor Details"  # Model description

    # Define fields for the model
    name = fields.Char(string="Name")  # Doctor's name
    partner_id = fields.Many2one('res.partner', string="Related Partner", required=True)  # Reference to related partner
    specialization = fields.Many2one('hospital.specialization', string="Specialization", required=True)  # Doctor's specialization
    license_no = fields.Char(string="License Number", required=True)  # Doctor's license number
    experience_years = fields.Integer(string="Experience (Years)", default=0)  # Years of experience
    hospital_id = fields.Many2one('hospital.details', string="Associated Hospital/Clinic", required=True)  # Associated hospital or clinic
    is_emergency_available = fields.Boolean(string="Emergency Available", default=False)  # Emergency availability

    # Constraint to validate the uniqueness of the license number
    @api.constrains('license_no')
    def validate_license_no(self):
        for records in self:
            if self.env['res.doctor'].search_count([('id', '!=', records.id), ('license_no', '=', records.license_no)]) > 0:
                raise ValidationError("Please Enter your Unique License No.")