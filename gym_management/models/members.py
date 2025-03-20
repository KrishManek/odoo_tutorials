from odoo import fields, models, api
from odoo.api import model_create_multi, constrains
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError,UserError


class Members(models.Model):
    _name = 'gym.members'
    _description = 'Members Information'

    check_in_ids = fields.One2many('gym.login.details','member_id','Check Ins')
    check_in_count = fields.Integer(compute='_compute_check_in_count',string='Check In Count',store=True)
    member_id = fields.Char(string='ID',readonly=True, default="New")
    name = fields.Char(string='Name', required=True)
    age = fields.Char(string='Age', compute='_compute_age',store=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')

    plan_id = fields.Many2one('gym.plans', string='Subscribed Plan')
    price = fields.Float(string="Plan Price", store =True)
    plan_type = fields.Selection([
        ('basic', 'Basic'),
        ('premium', 'Premium')
    ], string="Plan Type", required=True, default='basic')
    duration = fields.Selection([
        ('1_month', '1 Month'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('12_months', '12 Months')
    ], string="Duration", required=True)

    registration_date = fields.Date(string='Registration Date', default=fields.Date.today(),readonly=True)
    dob = fields.Date(string='Date of Birth')
    membership_expiry = fields.Date(string = 'Expiry' ,compute='_compute_expiry',store=True)

    trainer_id = fields.Many2one('gym.trainers', string='Trainer')
    trainer_name = fields.Char(string="Trainer Name", store=True)
    trainer_phone = fields.Char(string="Trainer Phone", store=True)
    trainer_experience = fields.Integer(string="Experience (Years)", store=True)
    trainer_specialization = fields.Char(string="Specialization", store=True)

    @model_create_multi
    def create(self,vals_list):
        res = super(Members,self).create(vals_list)
        for rec in res:
            rec.member_id = self.env['ir.sequence'].next_by_code('gym.members')
        return res

    @api.onchange('plan_id')
    def on_change_plan_id(self):
        self.price = self.plan_id.price
        self.plan_type = self.plan_id.plan_type
        self.duration = self.plan_id.duration

    @api.onchange('trainer_id')
    def on_change_trainer_id(self):
        self.trainer_phone = self.trainer_id.phone
        self.trainer_experience = self.trainer_id.experience
        self.trainer_specialization = self.trainer_id.specialization

    @api.depends('check_in_ids')
    def _compute_check_in_count(self):
        for record in self:
            record.check_in_count = self.env['gym.login.details'].search_count([('member_id','=',record.id)])

    def action_check_ins(self):
        form_view = self.env.ref('gym_management.log_in_form').id
        list_view = self.env.ref('gym_management.log_in_list').id

        res = {
            'name':'check-ins',
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'res_model':'gym.login.details',
            'view_id':form_view,
            'target':'current',
            'context':{'default_member_id':self.id}
        }

        if self.check_in_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view,'list'),(form_view,'form')]
            res['domain'] = [('member_id','=',self.id)]
            res['view_id'] = False
        return res

    def _welcome_reminder(self):
        new_members =[]
        result = self.env['gym.members'].search([('registration_date','=',fields.Date.today())])
        for rec in result:
            new_members.append(rec.name)
        print(f"Welcome to our gym {new_members}")

    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:
                diff = relativedelta(fields.Date.today(),record.dob)
                age_res = f"{diff.years} years {diff.months} months"
                record.age = age_res

    @api.constrains('phone')
    def check_phone(self):
        for record in self:
            if record.phone and len(record.phone) < 10:
                raise ValidationError("Phone number should be 10 digits")

            if record.phone:
                dup = self.env['gym.members'].search_count([('phone','=',record.phone)])
                if dup > 1:
                    raise UserError("Phone number already exists")

    @api.depends('registration_date','plan_id')
    def _compute_expiry(self):
        for record in self:
            if record.registration_date:
                if record.duration == '1_month':
                    record.membership_expiry = record.registration_date + relativedelta(months=1)
                elif record.duration == '3_months':
                    record.membership_expiry = record.registration_date + relativedelta(months=3)
                elif record.duration == '6_months':
                    record.membership_expiry = record.registration_date + relativedelta(months=6)
                elif record.duration == '12_months':
                    record.membership_expiry = record.registration_date + relativedelta(months=12)







