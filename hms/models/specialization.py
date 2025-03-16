from odoo import fields, models, api


class HospitalSpecialization(models.Model):
    _name = "hospital.specialization"
    _description = "Hospital Specialization"

    name = fields.Char(string="Specialization Name", required=True)
    description = fields.Text(string="Description")