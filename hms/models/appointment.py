from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class HmsAppointment(models.Model):
    _name = "appointment.details"
    _description = "Appointment"
    _rec_name = "patient_id"

    appointment_code = fields.Char(string="Appointment ID", copy=False, readonly=True, index=True, default="New")
    patient_id = fields.Many2one("patient.details", string="Patient", required=True)
    appointment_date = fields.Datetime(string="Date", required=True)
    appointment_reason = fields.Text(string="Reason")
    state = fields.Selection([('draft', 'Draft'),
                              ('wait','waiting'),
                              ('confirm', 'Confirm'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')], string="Status", default='draft')
    
    gaurdian_category = fields.Selection([('parent','Parent'),
                                          ('sibling','Sibbling'),
                                          ('relative','Relative'),
                                          ('friend','Friend'),
                                          ('other','Others')], string="Gaurdian Type")
    
    gaurdian_id = fields.Many2one('res.partner', string="Guardian Name")

    consultation_start_time = fields.Datetime(string = "Start Time")
    consultation_end_time = fields.Datetime(string = "end Time")
    consultation_time = fields.Float(string="Total Consultation Time")
    product_id = fields.Many2one('product.product', string ="Product")
    booking_time = fields.Datetime(string= "Booking Time", readonly=True)

    weekly_appointment_report_list = []
    weekly_cancelation_reports = {}

    @api.model_create_multi
    def create(self,vals_list):
        res = super(HmsAppointment,self).create(vals_list)
        for result in res:
            result.appointment_code = self.env['ir.sequence'].next_by_code('appointment.details')
            result.booking_time = fields.Datetime.now()
        return res
    
    @api.constrains('appointment_date')
    def validate_date(self):
        for record in self:
            if record.appointment_date.date() < fields.Date.today():
                raise ValidationError("Enter Select Future Date!")
            
    @api.constrains('appointment_date')
    def duplicate_appointments(self):
        for record in self:
            details = self.env['appointment.details'].search_count([('patient_id', '=', record.patient_id.id), 
                                                         ('appointment_date', '=', record.appointment_date)])
        if details > 1:
            raise ValidationError('Appointment Already exists! Please select another date')

    @api.onchange('patient_id')
    def on_change_patient(self):
        self.gaurdian_category = self.patient_id.gaurdian_category
        self.gaurdian_id = self.patient_id.gaurdian_id
    
    def action_wait_appointment(self):
        self.state = 'wait' 
    
    def action_confirm_appointment(self):
        self.state = 'confirm'
    
    def action_in_consultation(self):
        if self.appointment_date < fields.datetime.now():
            self.consultation_start_time = fields.datetime.now()
            self.state = 'in_consultation'
        else:
            raise ValidationError("Please wait for your consultation time")
        
    def action_done_appointment(self):
        if self.appointment_date < fields.datetime.now():
            self.consultation_end_time = fields.datetime.now()
            total_time = relativedelta(self.consultation_end_time, self.consultation_start_time)
            print(total_time.seconds)
            total_time_mins = total_time.hours * 60 + total_time.minutes + total_time.seconds/100
            self.state = 'done'
            self.consultation_time = total_time_mins
        else:
            raise ValidationError("Please wait for your consultation time")
        
    def action_cancel_appointment(self):
        self.state = 'cancel'
    
    def weekly_appointment_report(self):
        weekly_appointment_reports = {}
        today = fields.Date.today()
        seven_days_ago = today - relativedelta(days=7)
        details = self.env['appointment.details'].search([('consultation_start_time', '>=', seven_days_ago), 
                                                         ('consultation_start_time', '<=', today)])
        total_apointments = len(details)
        total_consultation_time = 0.00
        patients_time_hour_plus = 0
        for apointment in details:
            total_consultation_time += apointment.consultation_time 
            if apointment.consultation_time  > 60.00:
                patients_time_hour_plus += 1    
        weekly_appointment_reports['total_apointments'] = total_apointments
        weekly_appointment_reports['total_consultation_time'] = total_consultation_time
        weekly_appointment_reports['patients_time_hour_plus'] = patients_time_hour_plus
        self.weekly_appointment_report_list.append(weekly_appointment_reports)
        print(f"\n \n Details: {self.weekly_appointment_report_list}")

    def _auto_cancel_appointment(self):
        current = fields.Datetime.now()
        appointments = self.env['appointment.details'].search([('state', '=', 'draft'),
                                                               ('booking_time', '!=', False), 
                                                               ('booking_time', '<=', current - relativedelta(days=1))])
        if appointments:
            appointments.write({'state': 'cancel'})
            print(f"Cancelled {len(appointments)} draft appointments.")
        else:
            print("No appointments found for cancellation.")

    def weekly_cancelation_report(self):
        appointments = self.env['appointment.details'].search([('state', '=', 'cancel')])
        for details in appointments:
            self.weekly_cancelation_reports[details.appointment_code] = {'patient_id':details.patient_id,'appointment_date': details.appointment_date}
        print(self.weekly_cancelation_reports)