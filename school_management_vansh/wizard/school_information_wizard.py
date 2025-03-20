from odoo import models, fields

class SchoolOpeningWizard(models.TransientModel):
    _name = 'wizard.details'
    _description = 'School Opening Wizard'

    english_medium = fields.Char(string='English Medium')
    gujarati_medium = fields.Char(string='Gujarati Medium')


