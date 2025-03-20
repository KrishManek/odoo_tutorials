from odoo import fields, models, api


class HospitalSpecialization(models.Model):
    _name = 'hospital.specialization'
    _description = 'Hospital Specialization'

    name = fields.Char(string='Specialization', required=True)
    des_specialization = fields.Text(string='Description')