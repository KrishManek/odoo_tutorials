from odoo import models, fields, api


class HospitalDetails(models.Model):
    _name = 'hospital.hospital'
    _description = 'Hospital Information'

    name = fields.Char(string='Hospital Name', required=True)
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')
    is_public = fields.Boolean(string='Public Hospital')
    doctor_ids = fields.One2many('res.doctor', 'hospital_id', string='Doctors')