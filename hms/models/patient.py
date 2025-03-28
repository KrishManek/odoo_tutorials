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
    age_category = fields.Selection([('senior','Senior Citizen'),
                                     ('adult', 'Adult'),
                                     ('child', 'Child'),
                                     ('minor','Minor')],string= "Age Category")
    
    gaurdian_category = fields.Selection([('parent','Parent'),
                                          ('sibling','Sibbling'),
                                          ('relative','Relative'),
                                          ('friend','Friend'),
                                          ('other','Others')], string="Gaurdian Type")
    gaurdian_id = fields.Many2one('res.partner', string="Guardian Name")
    
    previous_diseases = fields.Text(string="Previous Diseases")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    appointment_ids = fields.One2many('appointment.details','patient_id',string="Appointment History")
    appointment_count = fields.Integer(compute="_compute_appointment_count", string="Appointment Count", store=True)
    weekly_visit = fields.Boolean(string="Weekly visit", default = False)
    partner_id = fields.Many2one('res.partner', string="Reference ID")
    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for patient in self:
            patient.appointment_count = self.env['appointment.details'].search_count([('patient_id','=', patient.id)])

    @api.model_create_multi
    def create(self,vals_list):
        for result in vals_list:
            result.update({'patient_code' :self.env['ir.sequence'].next_by_code('patient.details')})      
            partner = self.env['res.partner'].create([{
                'name':result.get('name'),
                'phone':result.get('phone'),
                'email':result.get('email')
            }])
            result.update({'partner_id':partner.id})
        res = super(PatientDetails,self).create(vals_list)            
        return res

    """ #open form in new page 
    def action_open_appointments(self):
        view_id = self.env.ref('hms.hms_appointment_form_view').id

        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'appointment.details',
            'view_id': view_id,
            'target': 'current',
            'context': {'default_patient_id': self.id},
        } """
    
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
            
    @api.onchange('date_of_birth')
    def on_change_dob(self):
        today = fields.Date.today()
        diff = relativedelta(today, self.date_of_birth) 
        self.age = f"{diff.years} years {diff.months} months"
        if diff.years >= 60:
            self.age_category = 'senior'
        elif diff.years >= 18:
            self.age_category = 'adult'
        elif diff.years >= 10:
            self.age_category = 'minor'
        elif diff.years < 10:
            self.age_category = 'child'
        else:
            raise ValidationError("please select correct dob")
        
    @api.constrains('age_category')
    def validate_gaurdian_fields(self):
        for records in self:
            if records.age_category == 'minor' or self.age_category == 'child':
                if not records.gaurdian_id or records.gaurdian_category:
                    raise ValidationError("Please Enter Guardian Details")

    
    def total_patients_above_40(self):
        today = fields.Date.today()
        forty_years_ago = today - relativedelta(years=40)
        patients_above_40 = self.env['patient.details'].search_count([('date_of_birth', '<=', forty_years_ago)])
        print(f"\n \n Total Patients above age 40 are : {patients_above_40}\n \n")

    def action_open_appointments(self):
        form_view_id = self.env.ref('hms.hms_appointment_form_view').id
        list_view_id = self.env.ref('hms.hms_appointment_list_view').id
        
        res = {
            'name' : 'Appointments',
            'type' : 'ir.actions.act_window',
            'view_mode' : 'form',
            'res_model' : 'appointment.details',
            'view_id' : form_view_id,
            'target' : 'current',
            'context' : {'default_patient_id' : self.id }
        }
        if self.appointment_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id,'list'),(form_view_id,'form')]
            res['domain'] = [('patient_id', '=', self.id)]
            res['view_id'] = False
        return res
    
    @api.model
    def weekly_appointment_creation(self):
        records = self.env['patient.details'].search([('weekly_visit', '=', True)])
        print("ABC")
        for appointment in records:
            self.env['appointment.details'].create([{
                'patient_id': appointment.id
            }])
        
    @api.model
    def write(self, vals):
        if self.env.context.get('from_partner_write'):
            return super().write(vals)
        res = super().write(vals)
        for patient in self:
            if 'phone' in vals or 'email' in vals:
                partner = patient.partner_id
                if partner:
                    partner.with_context(from_patient_write=True).write({
                        'phone': patient.phone,
                        'email': patient.email
                    })
        return res