from odoo import fields, models, api


class TutionFeeStructure(models.Model):
    _name = "tution.fee.structure"
    _description = "Tution Fee Structure"
    _res_name = 'product_id'
    

    product_id = fields.Many2one('product.template',string="Product")
    fee_amount = fields.Float(string="Fee Amount", store=True)
    quantity = fields.Float(string="Quantity", required=True, default=1.00)
    discount = fields.Float(string="Discount", required=True)
    sub_total = fields.Float(string="Sub Total",compute='_compute_sub_total', required=True, store=True)
    total = fields.Float(string="Total", compute='_compute_total', store=True)
    standard = fields.Selection([('one','1'),
                                 ('two','2'),
                                 ('three','3'),
                                 ('four','4'),
                                 ('five','5'),
                                 ('six','6'),
                                 ('seven','7'),
                                 ('eight','8'),
                                 ('nine','9'),
                                 ('ten','10'),
                                 ('eleven','11'),
                                 ('twelve','12')], required=True, string="Standard")
    
    @api.onchange('product_id')
    def _on_change_product(self):
        self.fee_amount = self.product_id.list_price
    
    @api.depends('fee_amount','quantity')
    def _compute_sub_total(self):
        for record in self:
            record.sub_total = self.fee_amount * self.quantity

    @api.depends('sub_total','discount')
    def _compute_total(self):
        for record in self:
            record.total  = record.sub_total - ((record.sub_total * record.discount) / 100)

