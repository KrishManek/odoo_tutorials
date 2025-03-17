from odoo import fields, models, api


class DoctorDetails(models.Model):
    _name = "res.doctor"  
    _inherit = 'res.partner'  
    _description = "Doctor Details"

    name = fields.Char(string = "Name")
    partner_id = fields.Many2one('res.partner', string="Related Partner", required=True)
    specialization = fields.Many2one('hospital.specialization', string="Specialization", required=True)
    license_no = fields.Char(string="License Number", required=True)
    experience_years = fields.Integer(string="Experience (Years)", default=0)
    hospital_id = fields.Many2one('hospital.details', string="Associated Hospital/Clinic", required=True)
    is_emergency_available = fields.Boolean(string="Emergency Available", default=False)