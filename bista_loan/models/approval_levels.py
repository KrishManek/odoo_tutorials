from odoo import models, fields, api

class ApprovalLevel(models.Model):
    _name = 'team.approval.level'
    _description = 'Approval Level Configuration'

    level = fields.Integer(string = 'Level', required = True)
    name = fields.Char(string = 'Name', required = True)
    user_ids = fields.Many2many('res.users', string = 'Users', domain = "[('id', 'not in', already_assigned_user_ids)]")
    team_id = fields.Many2one('approval.team', string = 'Team', ondelete = 'cascade')
    already_assigned_user_ids = fields.Many2many('res.users', compute = '_compute_user_domain', store = False)  
    
    @api.depends('team_id', 'user_ids')
    def _compute_user_domain(self):
        for rec in self:
            if rec.team_id:
                other_levels = self.search([
                    ('team_id', '=', rec.team_id.id)
                ])
                assigned_user_ids = set(other_levels.mapped('user_ids.id'))
                rec.already_assigned_user_ids = [(6, 0, list(assigned_user_ids))]
            else:
                rec.already_assigned_user_ids = [(6, 0, [])]
                
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('team_id'):
                existing_levels = self.search_count([('team_id', '=', vals['team_id'])])
                vals['level'] = existing_levels + 1
            else:
                vals['level'] = 1

        return super().create(vals_list)
            
            
