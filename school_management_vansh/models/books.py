from odoo import models, fields

class Books(models.Model):
    _name = 'books.details'
    _description = 'Books Details'
    _rec_name = 'book_name'

    book_name = fields.Char(string='Book Name', required=True)
    author = fields.Char(string='Author')
    qty = fields.Integer(string='Quantity')
    price = fields.Float(string='Price')

    book_id = fields.Many2one('school.details', string='Book Name')
    school_name = fields.Many2one('school.details', string='School Name', required=True)