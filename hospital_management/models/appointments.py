from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Appointments(models.Model):
    _name = 'hospital.appointments'
    _description = 'Appointments'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    appointment_id = fields.Char(string='Appointment ID',readonly=True)
    appointment_date = fields.Datetime(string='Appointment Date',default=fields.Date.today(),required=True)
    appointment_reason = fields.Text(string='Appointment Reason')

    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('waiting', 'Waiting'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')],
                             string="Status", default='draft')

    guardian_type = fields.Selection([('parent', 'Parent'), ('relative', 'Relative'),
                                      ('sibling', 'Sibling'), ('friend', 'Friend'), ('other', 'Other')],
                                     string='Guardian Type')

    guardian_id = fields.Many2one('res.partner', String='Guardian')
    start_consultation = fields.Datetime(string='In_Consultation')
    end_consultation = fields.Datetime(string='End_Consultation')
    total_consultation_time = fields.Float(string='Total Consultation Time')

    product_id = fields.Many2one('product.product', string='Product', domain=[('type' , '=' , 'service')])

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Appointments, self).create(vals_list)
        for record in res:
            record.appointment_id = self.env['ir.sequence'].next_by_code('hospital.appointments')
        return res

    @api.constrains('appointment_date')
    def check_appointment_date(self):
        for record in self:
            if record.appointment_date < fields.Date.today():
                raise ValidationError('Appointment Date should be greater than or equal to today')

    @api.constrains('patient_id')
    def duplicate_patient(self):
        for record in self:
            count_patient = self.env['hospital.appointments'].search_count(
                [('patient_id', '=', record.patient_id.id),
                 ('appointment_date', '=', record.appointment_date)])
            if count_patient > 1:
                raise ValidationError('Exists! Already a patient exists with this name')

    @api.onchange('patient_id')
    def on_change_patient_id(self):
        if self.patient_id:
            self.guardian_id = self.patient_id.guardian_id
            self.guardian_type = self.patient_id.guardian_type

    def action_confirm(self):
        self.state = 'confirm'

    def action_in_consultation_(self):
        self.state = 'in_consultation'
        self.start_consultation = datetime.now()

    def action_done(self):
        if self.appointment_date < fields.datetime.now():
            self.end_consultation = fields.datetime.now()
            total_time = relativedelta(self.end_consultation, self.start_consultation)
            total_time_mins = total_time.hours * 60 + total_time.minutes + total_time.seconds / 100
            self.state = 'done'
            self.total_consultation_time = total_time_mins
        else:
            raise ValidationError("Please wait for your consultation time")

    def action_cancel(self):
        self.state = 'cancel'

    def _Check_appointments(self):
        for record in self:
            if record.state == 'draft':
                if fields.Date.today() > record.appointment_date:
                    record.state = 'cancel'

    def _Cancelled_Appointments(self):
        cancelled_appointments = {}
        today = fields.Date.today()
        seven_days = today - relativedelta(days=7)
        appointments = self.env['hospital.appointments'].search([('state','=','cancel'),
                                                                 ('appointment_date','<=',today),
                                                                 ('appointment_date','>=',seven_days)])

        for appt in appointments:
            cancelled_appointments[appt.appointment_id] = {'patient_id':appt.patient_id.name,'appointment_date':appt.appointment_date}
        print(cancelled_appointments)

    def _Consultation_Report(self):
        week_report = {}
        today = fields.Date.today()
        diff_seven_days = today - relativedelta(days=7)

        appointments = self.env['hospital.appointments'].search([
            ('start_consultation', '>=', diff_seven_days),
            ('end_consultation', '<=', today)
        ])

        total_con = len(appointments)
        total_time = 0.00
        patient = []

        for app in appointments:
            total_time += app.total_consultation_time
            if app.total_consultation_time > 60.00:
                patient.append(app.patient_id.name)

        week_report['totalappointment'] = total_con
        week_report['total_time'] = total_time
        week_report['patient_time_hour_plus'] = patient
        print(week_report)







