from email.policy import default

from odoo import fields, models, api


class Prescription(models.Model):
    _name = 'prescription_details'
    _description = 'prescription Information'


    patient_id = fields.Many2one('hospital.patient', string='Patient')
    date = fields.Datetime(string='Date', required=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('cancel','Cancelled'),
    ],default='draft',string='Status')
    prescription_lines = fields.One2many('prescription_line.details','prescription_id',string='Prescriptions')

    def action_confirm(self):
        self.state = 'confirm'

    def action_cancel(self):
        self.state = 'cancel'