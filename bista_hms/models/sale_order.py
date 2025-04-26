from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    lead_reference = fields.Char(string="Lead Reference")
    discount_amount = fields.Float(string="Discount Amount")


    @api.depends('order_line.price_subtotal', 'currency_id', 'company_id', 'discount_amount')
    def _compute_amounts(self):
        res = super(SaleOrder, self)._compute_amounts()
        for order in self:
            order.amount_total = order.amount_total - order.discount_amount
        return res


    def _prepare_invoice(self):
        vals = super(SaleOrder, self)._prepare_invoice()
        vals['lead_referral'] = self.lead_reference
        return vals