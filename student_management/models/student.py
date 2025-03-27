from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta


class StudentDetails(models.Model):
    _name = "res.student"
    _description = "Student Res Model"

    registration_code = fields.Char(string="Registration ID", default = "New")
    name = fields.Char(String="name", required=True)
    registration_date = fields.Date(string="Registration Date:", default=fields.Date.today())
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    age = fields.Char(string="Age", compute ='_compute_age', store=True)
    phone = fields.Char(string="Phone No.")
    email = fields.Char(string="Email")
    standard = fields.Selection([('one','1'),
                                          ('two','2'),
                                          ('three','3'),
                                          ('four','4'),
                                          ('five','5'),
                                          ('six','6'),
                                          ('seven','7'),
                                          ('eight','8'),
                                          ('nine','9'),
                                          ('ten','10'),
                                          ('eleven','11'),
                                          ('twelve','12')], string="Standard")
    tution_fee_structure = fields.Many2one("tution.fee.structure", string="Tution Fee")
    gaurdian_name = fields.Char(string="Guardian Name")
    gaurdian_phone = fields.Char(string="Guardian Phone No.")
    is_blocked = fields.Boolean(string="IS Blocked", default = False)
    is_expired = fields.Boolean(string="IS Expired", default = False)
    is_child = fields.Boolean(default=False)
    previous_year_marks = fields.One2many('previous.years.marks','student_id', string="Previous Year Marks" )

    @api.model_create_multi
    def create(self,vals_list):
        res = super(StudentDetails,self).create(vals_list)
        for result in res:
            result.registration_code = self.env['ir.sequence'].next_by_code('res.student')
        return res
    
    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            today = fields.Date.today()
            diff = relativedelta(today, record.date_of_birth) 
            if(diff.years<10):
                record.is_child = True
            record.age = f"{diff.years} years, {diff.months} months"
            record.age_years = diff.years
    
    @api.constrains('phone')
    def check_phone(self):
        for record in self:
            if record.phone.isnumeric():
                if record.phone and len(record.phone) < 10:
                    raise UserError("Phone number should be minimum 10 digits")
                else:
                    student_ids = self.env['res.student'].search_count([('phone', '=', record.phone),('id', '!=', record.id)])
                    if student_ids:
                        raise UserError("Phone number already exists! Please Enter your own phone no.")
            else:
                raise ValidationError("Please enter phone no in digits only")
            
    def action_is_blocked(self):
        self.is_blocked = False

    def action_is_not_blocked(self):
        self.is_blocked = True

    def write(self, vals):
        for record in self:
            if record.is_blocked and 'is_blocked' not in vals:
                raise UserError("Blocked students cannot edit their details.")
        res = super().write(vals)
        return res

    def student_registration_expied(self):
        expiry_month = self.registration_date - relativedelta(days=30)
        expired_students = self.env['res.student'].search([('registration_date', '<=', expiry_month),('is_blocked','!=',True)])
        for students in expired_students:
            students.is_expired = True             
