from odoo import fields, models, api
from odoo.exceptions import ValidationError

class HotelRoomCategory(models.Model):
    _name = 'hotel.room.category'
    _description = 'Hotel Room Category'

    name = fields.Char(string="Category Name", copy=False, required=True)
    price = fields.Float(string="Default Room Price", required=True)

    @api.constrains('price')
    def _check_positive_price(self):
        for rec in self:
            if rec.price <= 0:
                raise ValidationError("Room price must be a positive number.")
    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            if rec.name:
                existing = self.search([('name', '=', rec.name),('id', '!=', rec.id)])
                if existing:
                    raise ValidationError("Category name must be unique.")

