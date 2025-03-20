from odoo import models, fields, api
from odoo.api import constrains
from odoo.exceptions import ValidationError

class Doctor(models.Model):
    _name = 'res.doctor'
    _description = 'Doctor Information'
    # _inherit = 'res.partner'

    name = fields.Char(string='Doctor Name',required=True)
    specialization = fields.Many2one('hospital.specialization', string='Specialization')
    license_no = fields.Char(string='License Number')
    experience_years = fields.Integer(string='Experience in Years')
    hospital_id = fields.Many2one('hospital.hospital', string='Associated Hospital/Clinic')
    is_emergency_available = fields.Boolean(string='Emergency Availability')

    @api.constrains('license_no')
    def unique_license_no(self):
        for record in self:
            if self.env['res.doctor'].search_count([('id', '!=', record.id),('license_no','=',record.license_no)]) > 0:
                raise ValidationError("License Number must be unique")




