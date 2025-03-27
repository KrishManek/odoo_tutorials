from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError


class HmsAppointment(models.Model):
    _name = "hms.appointment"
    _description = "Appointment"
    _rec_name = "patient_id"

    name = fields.Char(string="Appointment ID", copy=False, readonly=True, index=True, default="New")
    patient_id = fields.Many2one("res.patient", string="Patient", required=True, ondelete="restrict")
    phone = fields.Char(string="Phone")
    appointment_date = fields.Datetime(string="Date", required=True)
    appointment_reason = fields.Text(string="Reason")
    state = fields.Selection([('draft', 'Draft'),
                                           ('confirm', 'Confirm'),
                                           ('waiting', 'Waiting'),
                                           ('in_consultation', 'In Consultation'),
                                           ('done', 'Done'),
                                           ('cancel', 'Cancel')],
                                          string="Status", default='draft')

    def _send_appointment_reminder_today(self):
        # Send appointment reminder to patients
        # This method will be called by a cron job
        start_day = datetime.today().replace(hour=0, minute=0, second=1, microsecond=0)
        end_day = datetime.today().replace(hour=23, minute=59, second=59, microsecond=0)
        appointment_ids = self.env['hms.appointment'].search([('appointment_date', '>=', start_day),
                                                              ('appointment_date', '<=', end_day),])

        print(appointment_ids)

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            self.phone = self.patient_id.phone

    def action_confirm(self):
        print("context=========", self._context, ) #self.env.context
        self.state = 'confirm'

    def unlink(self):
        # for rec in self:
        #     if rec.state not in ['draft', 'cancel']:
        #         raise ValidationError("You can not delete a record which is not in draft or cancel state")
        #
        check_ids = self.filtered(lambda s: s.state not in ['draft', 'cancel'])
        if check_ids:
            raise ValidationError("You can not delete a record which is not in draft or cancel state")
        return super(HmsAppointment, self).unlink()

