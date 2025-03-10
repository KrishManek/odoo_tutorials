from odoo import fields, models
class SchoolDetails(models.Model):
    _name = "school.details"
    _description = "School_Details"

    name = fields.Char(String="name")
    desc = fields.Text(String="Description")