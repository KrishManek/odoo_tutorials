from odoo import models, fields,api

class GymPlan(models.Model):
    _name = 'gym.plans'
    _description = 'Gym Membership Plan'

    name = fields.Char(string="Plan Name", required=True)
    plan_type = fields.Selection([
        ('basic', 'Basic'),
        ('premium', 'Premium')
    ], string="Plan Type", required=True, default='basic')
    price = fields.Float(string="Plan Price", required=True, compute='_on_compute_price', store=True)
    duration = fields.Selection([
        ('1_month', '1 Month'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('12_months', '12 Months')
    ], string="Duration", required=True)
    member_ids = fields.One2many('gym.members', 'plan_id', string="Subscribed Members")

    @api.depends('plan_type','duration')
    def _on_compute_price(self):
        for rec in self:
            if rec.plan_type =='basic' and rec.duration == '1_month':
                rec.price = 1000
            elif rec.plan_type =='basic' and rec.duration == '3_months':
                rec.price = 2850
            elif rec.plan_type =='basic' and rec.duration == '6_months':
                rec.price = 5400
            elif rec.plan_type =='basic' and rec.duration == '12_months':
                rec.price = 10200
            elif rec.plan_type =='premium' and rec.duration == '1_month':
                rec.price = 1500
            elif rec.plan_type =='premium' and rec.duration == '3_months':
                rec.price = 4300
            elif rec.plan_type =='premium' and rec.duration == '6_months':
                rec.price = 8100
            elif rec.plan_type =='premium' and rec.duration == '12_months':
                rec.price = 15300


