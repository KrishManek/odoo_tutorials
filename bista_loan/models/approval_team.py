from odoo import models, fields, api


class ApprovalTeam(models.Model):
    _name = 'approval.team'
    _description = 'Approval Team Configuration'

    name = fields.Char(string='Team Name', required=True)
    approval_level_ids = fields.One2many('team.approval.level', 'team_id', string='Approval Levels')
