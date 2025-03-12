from odoo import fields,models
class standardDetails(models.Model):
    _name = "standard.details"
    _description = "Standard_Details"

    division = fields.Char(String="Division")
    standard = fields.Integer(String="Srandard")
    std_id = fields.Many2one('teacher.details', String="Teaches in")
    