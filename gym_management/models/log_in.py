from odoo import fields, models, api
from  dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError


class LogIn(models.Model):
    _name = 'gym.login.details'
    _description = 'Login Details'
    _rec_name = 'member_id'

    # date_today = fields.Date(string='Date',required=True)
    check_in_time = fields.Datetime(string='Check In',default=fields.Datetime.now())
    check_out_time = fields.Datetime(string='Check Out')
    total_time = fields.Float(string='Total Time',compute='_compute_total_time',store=True)
    member_id = fields.Many2one('gym.members','Name')
    state = fields.Selection([
        ('new','New'),
        ('check_in','Check In'),
        ('check_out','Check Out')
    ],default='new',string='Status')

    def action_log_in(self):
        if not self.member_id.membership_expiry < fields.Date.today():
            self.state = 'check_in'
            self.check_in_time = fields.Datetime.now()
        else:
            raise UserError("Membership Expired")


    def action_log_out(self):
        self.state = 'check_out'
        self.check_out_time = fields.Datetime.now()

    @api.depends('check_in_time','check_out_time')
    def _compute_total_time(self):
        for rec in self:
            in_time = rec.check_in_time
            out_time = rec.check_out_time
            total = relativedelta(out_time,in_time)
            rec.total_time = total.hours * 60 + total.minutes + total.seconds/100

    @api.constrains('check_in_time')
    def double_checkin_restrict(self):
        for record in self:
            double = self.env['gym.login.details'].search_count([('state','=','check_in'),('member_id','=',record.member_id.id)])
            if double > 1 :
                raise UserError("You can't check in twice")








