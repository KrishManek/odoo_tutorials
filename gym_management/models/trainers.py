from odoo import models, fields, api


class Trainers(models.Model):
    _name = 'gym.trainers'
    _description = 'Trainers Information'

    trainer_id = fields.Char(string='Trainer ID', readonly=True, default="New")
    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    experience = fields.Integer(string='Experience')
    specialization = fields.Selection([
        ('yoga', 'Yoga'),
        ('cardio', 'Cardio'),
        ('strength', 'Strength'),
       ])
    salary = fields.Float(string='Salary')
    member_ids = fields.One2many('gym.members', 'trainer_id', string='Members')
    member_count = fields.Integer(compute='_compute_member_count', string='Member Count', store=True)

    def create(self,vals_list):
        res = super(Trainers,self).create(vals_list)
        for rec in res:
            rec.trainer_id = self.env['ir.sequence'].next_by_code('gym.trainers')
        return res

    @api.depends('member_ids')
    def _compute_member_count(self):
        for record in self:
            record.member_count = self.env['gym.members'].search_count([('trainer_id','=',record.id)])

    def action_open_members(self):
        form_view = self.env.ref('gym_management.view_members_form').id
        list_view = self.env.ref('gym_management.view_members_list').id

        res = {
            'name' : 'members',
            'type' : 'ir.actions.act_window',
            'view_mode' : 'form',
            'res_model' : 'gym.members',
            'view_id' : form_view,
            'target' : 'current',
            'context' : {'default_member_id' : self.id}
        }

        if self.member_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view,'list'),(form_view,'form')]
            res['domain'] = [('trainer_id','=',self.id)]
            res['view_id'] = False
        return res

