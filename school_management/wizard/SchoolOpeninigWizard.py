from odoo import fields,models
class SchoolOpeningWizard(models.TransientModel):
    _name = "school.opening.wizard"
    _description = "School opening Wizard"

    start_date = fields.Date(string = "Start Date", required = True)
    end_date = fields.Date(string = "End Date")