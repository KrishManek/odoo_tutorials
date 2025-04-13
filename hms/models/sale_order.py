from odoo import fields,models,api
from num2words import num2words 
class SaleOrder(models.Model):
    _inherit = 'sale.order'


    lead_reference = fields.Char(string="Lead Reference")
    amount_in_words = fields.Char(string="Amount in Words", compute="_compute_amount_in_words")
    total_discount_amount = fields.Monetary(string='Total Discount', compute='_compute_total_discount_amount', store=True, currency_field='currency_id')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            partner_id = vals.get('partner_id')
            if partner_id:
                partner = self.env['res.partner'].browse(partner_id)
                if partner.use_customers_tc and partner.terms_and_conditions:
                    vals['note'] = partner.terms_and_conditions
        return super(SaleOrder, self).create(vals_list)
    
    @api.depends('amount_total')
    def _compute_amount_in_words(self):
        for rec in self:
            rec.amount_in_words = num2words(rec.amount_total, lang="en_IN",to="currency", currency="INR").title().replace(',',' ')
            #rec.amount_in_words = rec.currency_id.amount_to_text(rec.amount_total)
    
    @api.depends('order_line.price_unit', 'order_line.product_uom_qty', 'order_line.discount')
    def _compute_total_discount_amount(self):
        for order in self:
            total_discount = 0.0
            for line in order.order_line:
                line_discount = (line.price_unit * line.product_uom_qty) * (line.discount / 100)
                total_discount += line_discount
            order.total_discount_amount = total_discount
