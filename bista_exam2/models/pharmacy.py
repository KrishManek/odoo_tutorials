from odoo import fields, models,api
from odoo.exceptions import UserError

class Pharmacy(models.Model):
    _name = 'bista.pharma'
    _description = 'Bista Pharmacy'
    
    name = fields.Char(string="Name")

    @api.constrains('name')
    def check_name(self):
        for record in self:
            if record.name:
                duplicate = self.env['bista.pharma'].search_count([('name', '=', record.name),('id', '!=', record.id)])
                if duplicate:
                    raise UserError("Name number already exists!")
            