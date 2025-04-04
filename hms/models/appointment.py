from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


# Define the HmsAppointment model
class HmsAppointment(models.Model):
    _name = "appointment.details"  # Model name
    _description = "Appointment"  # Model description
    _rec_name = "patient_id"  # Field used for record name

    # Define fields for the model
    appointment_code = fields.Char(string="Appointment ID", copy=False, readonly=True, index=True, default="New")  # Appointment code
    patient_id = fields.Many2one("patient.details", string="Patient", required=True)  # Reference to patient details
    appointment_date = fields.Datetime(string="Date", required=True, default=(fields.Datetime.now() + relativedelta(hour=1)))  # Appointment date
    appointment_reason = fields.Text(string="Reason")  # Reason for appointment
    state = fields.Selection([('draft', 'Draft'),
                              ('wait', 'waiting'),
                              ('confirm', 'Confirm'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')], string="Status", default='draft')  # Appointment state
    
    gaurdian_category = fields.Selection([('parent', 'Parent'),
                                          ('sibling', 'Sibling'),
                                          ('relative', 'Relative'),
                                          ('friend', 'Friend'),
                                          ('other', 'Others')], string="Guardian Type")  # Guardian type
    
    gaurdian_id = fields.Many2one('res.partner', string="Guardian Name")  # Reference to guardian details

    consultation_start_time = fields.Datetime(string="Start Time")  # Consultation start time
    consultation_end_time = fields.Datetime(string="End Time")  # Consultation end time
    consultation_time = fields.Float(string="Total Consultation Time")  # Total consultation time
    product_id = fields.Many2one('product.product', string="Product")  # Reference to product details
    booking_time = fields.Datetime(string="Booking Time", readonly=True)  # Booking time

    weekly_appointment_report_list = []  # List to store weekly appointment reports
    weekly_cancelation_reports = {}  # Dictionary to store weekly cancellation reports
    doctor_id = fields.Many2one('res.doctor' ,string="Doctor name")

    # Override the create method to generate a unique appointment code and set booking time
    @api.model_create_multi
    def create(self, vals_list):
        res = super(HmsAppointment, self).create(vals_list)
        for result in res:
            result.appointment_code = self.env['ir.sequence'].next_by_code('appointment.details')
            result.booking_time = fields.Datetime.now()
        return res
    
    # Constraint to validate the appointment date
    @api.constrains('appointment_date')
    def validate_date(self):
        for record in self:
            if record.appointment_date.date() < fields.Date.today():
                raise ValidationError("Enter Select Future Date!")
            
    # Constraint to check for duplicate appointments
    @api.constrains('appointment_date')
    def duplicate_appointments(self):
        for record in self:
            details = self.env['appointment.details'].search_count([('patient_id', '=', record.patient_id.id), 
                                                                     ('appointment_date', '=', record.appointment_date)])
            if details > 1:
                raise ValidationError('Appointment Already exists! Please select another date')

    # On change event to update guardian details based on patient
    @api.onchange('patient_id')
    def on_change_patient(self):
        self.gaurdian_category = self.patient_id.gaurdian_category
        self.gaurdian_id = self.patient_id.gaurdian_id
    
    # Action to set appointment state to 'waiting'
    def action_wait_appointment(self):
        self.state = 'wait' 
    
    # Action to set appointment state to 'confirm'
    def action_confirm_appointment(self):
        self.state = 'confirm'
    
    # Action to set appointment state to 'in consultation' and record start time
    def action_in_consultation(self):
        if self.appointment_date < fields.Datetime.now():
            self.consultation_start_time = fields.Datetime.now()
            self.state = 'in_consultation'
        else:
            raise ValidationError("Please wait for your consultation time")
        
    # Action to set appointment state to 'done' and record end time and total consultation time
    def action_done_appointment(self):
        if self.appointment_date < fields.Datetime.now():
            self.consultation_end_time = fields.Datetime.now()
            total_time = relativedelta(self.consultation_end_time, self.consultation_start_time)
            total_time_mins = total_time.hours * 60 + total_time.minutes + total_time.seconds / 100
            self.state = 'done'
            self.consultation_time = total_time_mins
        else:
            raise ValidationError("Please wait for your consultation time")
        
    # Action to set appointment state to 'cancel'
    def action_cancel_appointment(self):
        self.state = 'cancel'
    
    # Method to generate weekly appointment report
    def weekly_appointment_report(self):
        weekly_appointment_reports = {}
        today = fields.Date.today()
        seven_days_ago = today - relativedelta(days=7)
        details = self.env['appointment.details'].search([('consultation_start_time', '>=', seven_days_ago), 
                                                          ('consultation_start_time', '<=', today)])
        total_appointments = len(details)
        total_consultation_time = 0.00
        patients_time_hour_plus = 0
        for appointment in details:
            total_consultation_time += appointment.consultation_time 
            if appointment.consultation_time > 60.00:
                patients_time_hour_plus += 1    
        weekly_appointment_reports['total_appointments'] = total_appointments
        weekly_appointment_reports['total_consultation_time'] = total_consultation_time
        weekly_appointment_reports['patients_time_hour_plus'] = patients_time_hour_plus
        self.weekly_appointment_report_list.append(weekly_appointment_reports)
        print(f"\n \n Details: {self.weekly_appointment_report_list}")

    # Method to automatically cancel draft appointments older than one day
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

    # Method to generate weekly cancellation report
    def weekly_cancelation_report(self):
        appointments = self.env['appointment.details'].search([('state', '=', 'cancel')])
        for details in appointments:
            self.weekly_cancelation_reports[details.appointment_code] = {'patient_id': details.patient_id.name, 'appointment_date': details.appointment_date}
        print(self.weekly_cancelation_reports)

    def daily_appointment_vals(self):
        today = fields.Datetime.today()
        tommorrow = today + relativedelta(1)
        start_time = tommorrow.replace(hour=0,minute=0,second=0, microsecond=1)
        end_time = tommorrow.replace(hour=23,minute=59,second=59, microsecond=9)
        appointments = self.env['appointment.details'].search([('appointment_date', '>=', start_time),('appointment_date', '<=', end_time)])
        return appointments
    
    def daily_appointment(self):
        template_id = self.env.ref('hms.email_template_appointment_confirmation')
        template_id.send_mail(self.id, force_send=True)
