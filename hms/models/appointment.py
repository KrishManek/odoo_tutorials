from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HmsAppointment(models.Model):
    _name = "appointment.details"
    _description = "Appointment"
    _rec_name = "patient_id"

    appointment_code = fields.Char(string="Appointment ID", copy=False, readonly=True, index=True, default="New")
    patient_id = fields.Many2one("patient.details", string="Patient", required=True)
    appointment_date = fields.Date(string="Date", required=True)
    appointment_reason = fields.Text(string="Reason")
    state = fields.Selection([('draft', 'Draft'),
                                           ('confirm', 'Confirm'),
                                           ('waiting', 'Waiting'),
                                           ('in_consultation', 'In Consultation'),
                                           ('done', 'Done'),
                                           ('cancel', 'Cancel')],
                                          string="Status", default='draft')
    
    @api.model_create_multi
    def create(self,vals_list):
        res = super(HmsAppointment,self).create(vals_list)
        for result in res:
            result.appointment_code = self.env['ir.sequence'].next_by_code('appointment.details')
        return res
    
    @api.constrains('appointment_date')
    def validate_date(self):
        for record in self:
            if record.appointment_date < fields.Date.today():
                raise ValidationError("Enter Select Future Date!")