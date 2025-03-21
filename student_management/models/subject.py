from odoo import fields, models


class SubjectDetails(models.Model):
    _name = "subject.subject"
    _description = "subject Res Model"

    name = fields.Char(String="name", required=True)