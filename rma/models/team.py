from odoo import fields, models, api
from odoo.exceptions import ValidationError

class RMATeam(models.Model):
    _name = "rma.team"
    _description = "RMA Team"


    name = fields.Char(string="Member Name", required=True)
    code = fields.Char(string="Team Name", required=True)
    sequence_preview = fields.Char(string="Next RMA Sequence", compute="_compute_sequence_preview")

    @api.model_create_multi
    def create(self, vals_list):
        teams = super().create(vals_list)
        for team in teams:
            prefix = f'{team.code}/{team.name}'
            seq_code = f'rma.team.{team.id}'
            # Check if sequence already exists
            existing_seq = self.env['ir.sequence'].search([('code', '=', seq_code)], limit=1)
            if not existing_seq:
                self.env['ir.sequence'].create({
                    'name': f'RMA Sequence for {team.name}',
                    'code': seq_code,
                    'prefix': prefix,
                    'padding': 4,
                })
        return teams

    @api.depends('code', 'name')
    def _compute_sequence_preview(self):
        for team in self:
            seq_code = f'rma.team.{team.id}'
            sequence = self.env['ir.sequence'].search([('code', '=', seq_code)], limit=1)
            if sequence:
                team.sequence_preview = sequence.prefix
            else:
                team.sequence_preview = "-"