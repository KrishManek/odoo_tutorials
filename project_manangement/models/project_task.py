# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    allocated_hours = fields.Float(string="Allocated Hours", required=True)
    date_deadline = fields.Date(string="Deadline", required=True)

    pr_link = fields.Char(string='PR Link')
    module_name = fields.Char(string='Module Name')
    developer_notes = fields.Text(string='Developer Notes')

    is_staging = fields.Boolean(
        string="Is in Staging or Later",
        compute="_compute_is_staging",
        store=True
    )

    # Validation for allocated hours > 0
    @api.constrains('allocated_hours')
    def _check_allocated_hours(self):
        for task in self:
            if task.allocated_hours <= 0:
                raise ValidationError("Allocated Hours must be greater than zero.")

    # Validation for deadline not in past
    @api.constrains('date_deadline')
    def _check_date_deadline(self):
        for task in self:
            if task.date_deadline and task.date_deadline < fields.Date.today():
                raise ValidationError("Deadline cannot be in the past.")

    # Constrain for required fields if task is in staging or later
    @api.constrains('pr_link', 'module_name', 'developer_notes')
    def _check_required_in_staging(self):
        for task in self:
            if task.is_staging:
                missing = []
                if not task.pr_link:
                    missing.append("PR Link")
                if not task.module_name:
                    missing.append("Module Name")
                if not task.developer_notes:
                    missing.append("Developer Notes")
                if missing:
                    raise ValidationError(
                        f"The following fields are required in 'Staging' or later: {', '.join(missing)}"
                    )

    # Compute if task is in staging or later
    @api.depends('stage_id', 'stage_id.is_staging')
    def _compute_is_staging(self):
        for task in self:
            task.is_staging = bool(task.stage_id and task.stage_id.is_staging)

    # Onchange warning for missing fields in staging or later
    @api.onchange('stage_id')
    def _onchange_stage_warning(self):
        if self.stage_id and self.stage_id.is_staging:
            missing_fields = []
            if not self.pr_link:
                missing_fields.append("PR Link")
            if not self.module_name:
                missing_fields.append("Module Name")
            if not self.developer_notes:
                missing_fields.append("Developer Notes")
            if missing_fields:
                return {
                    'warning': {
                        'title': "Missing Required Fields",
                        'message': "{} {} required in 'Staging' or later stage.".format(
                            ", ".join(missing_fields),
                            "is" if len(missing_fields) == 1 else "are"
                        ),
                    }
                }


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    is_staging = fields.Boolean(string="Is Staging or Later Stage")
