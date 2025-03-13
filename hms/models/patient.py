from odoo import fields, models, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class PatientDetails(models.Model):
    _name = "patient.details"
    _description = "Patient_Details"

    patient_code = fields.Char(string="Patient ID", default = "New")
    name = fields.Char(String="name", required=True)
    blood_group = fields.Selection([('A+', 'A+ve'),
                ('B+', 'B+ve'),
                ('O+', 'O+ve'),
                ('AB+', 'AB+ve'),
                ('A-', 'A-ve'),
                ('B-', 'B-ve'),
                ('O-', 'O-ve'),
                ('AB-', 'AB-ve')], string="Blood Group", default = 'O+',required=True)
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    age = fields.Char(string="Age")
    previous_diseases = fields.Text(string="Previous Diseases")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")

    @api.model_create_multi
    def create(self,vals_list):
        res = super(PatientDetails,self).create(vals_list)
        for result in res:
            result.patient_code = self.env['ir.sequence'].next_by_code('patient.details')
        return res
    
    def action_open_appointments(self):
        view_id = self.env.ref('hms.hms_appointment_form_view').id

        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'appointment.details',
            'view_id': view_id,
            'target': 'current',
        }
    
    def action_calculate_age(self):
        for record in self:
            if not record.date_of_birth:
                raise ValidationError("Please enter a Date of Birth before calculating age.")
            today = fields.Date.today()
            diff = relativedelta(today, record.date_of_birth) 
            self.age = f"{diff.years} years {diff.months} months"

    @api.constrains('date_of_birth')
    def validate_date(self):
        for record in self:
            if record.date_of_birth > fields.Date.today():
                raise ValidationError("Enter Select Correct Date of Birth!")
            else:
                today = fields.Date.today()
                diff = relativedelta(today, record.date_of_birth) 
                self.age = f"{diff.years} years {diff.months} months"