from odoo import fields,models,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    orignal_price = fields.Float(string="Orignal Price", compute="_compute_previous_price", store=True)
    
    @api.depends('product_id', 'product_uom', 'product_uom_qty', 'order_partner_id.extra_discount')
    def _compute_discount(self):
        res = super(SaleOrderLine,self)._compute_discount()
        for order in self:
            order.discount += order.order_partner_id.extra_discount
        return res

    @api.depends('product_template_id','product_id.lst_price')
    def _compute_previous_price(self):
        for rec in self:
            rec.orignal_price = rec.product_id.lst_price