# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProjectEstimationLine(models.Model):
    _name = 'project.estimation.line'
    _description = 'Project Estimation Line'
    _inherit = ["mail.thread", 'mail.activity.mixin']

    project_id = fields.Many2one('project.estimation', string="Project Id", help="Project id")
    # product_id = fields.Many2one('product.product', required=True, string="Product", help="product id for the project")
    product_id = fields.Many2one('product.product', required=True, string="Product", domain="[('id', 'not in', parent.dup_product)]", help="product id for the project")
    #dup_product = fields.Many2many('product.product', string="duplicate_products", compute="")
    note = fields.Char(string='Note', help="Sale order Description")
    quantity = fields.Integer(string="Quantity", required=True, tracking=True, default=1, help="no of products required")
    price = fields.Float(string="Unit Price",  tracking=True, help="Price per Product")
    sub_total = fields.Float(string="SubTotal", compute="_compute_sub_total", store=True, help="Subtotal for qty * price")

    @api.onchange('product_id')
    def on_change_product_id(self):
        """
        Automatically update values for price and note
        """
        self.price = self.product_id.lst_price
        self.note = self.product_id.description_sale
    
    @api.depends('quantity', 'price')
    def _compute_sub_total(self):
        """
        coomputes sub total = price * quantity
        """
        
        for record in self:
            record.sub_total = record.price * record.quantity
            
    @api.constrains('quantity')
    def check_quantity(self):
        """
            checks for negative quantity
        Raises:
            ValidationError: Quantity can't be negative"
        """
        for record in self:
            if record.quantity < 0:
                raise ValidationError("Quantity can't be negative")
            
    @api.constrains('price')
    def check_price(self):
        """
        checks for negative price
        Raises:
            ValidationError: _descPrice can't be negativeription_
        """
        for record in self:
            if record.price < 0:
                raise ValidationError("Price can't be negative")
    
    """     @api.depends('product_id','project_id')
    def _duplicate_products(self):
        for rec in self:
            rec.dup_product = [(5, 0, 0)]
            products = self.env['project.estimation.line'].search([('project_id', '=', self.id)]).mapped('product_id')
            rec.dup_product = [(4, 0, products.ids)]
            print(rec.dup_product) """