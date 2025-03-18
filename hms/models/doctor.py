from odoo import fields, models, api
from odoo.exceptions import ValidationError

class DoctorDetails(models.Model):
    _name = "res.doctor"    
    _description = "Doctor Details"

    name = fields.Char(string = "Name")
    partner_id = fields.Many2one('res.partner', string="Related Partner", required=True)
    specialization = fields.Many2one('hospital.specialization', string="Specialization", required=True)
    license_no = fields.Char(string="License Number", required=True)
    experience_years = fields.Integer(string="Experience (Years)", default=0)
    hospital_id = fields.Many2one('hospital.details', string="Associated Hospital/Clinic", required=True)
    is_emergency_available = fields.Boolean(string="Emergency Available", default=False)

    api.constrains('license_no')
    def validate_license_no(self):
        for records in self:
            if self.env['res.doctor'].search_count([('id','!=',records.id),('license_no','=',records.license_no)]) > 0:
                raise ValidationError("Please Enter your Unique License No.")