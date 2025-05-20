from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    def _get_display_price_ignore_combo(self):
        self.ensure_one()
        base_display_price = super()._get_display_price_ignore_combo()
        special_pricelist = self.env['product.pricelist'].search([('special_pricelist', '=', True),('active', '=', True)], limit=1)
        special_price = 0.0
        if special_pricelist:
            special_price = self._get_price_from_pricelist(special_pricelist)
        return max(base_display_price, special_price)
    
    def _get_price_from_pricelist(self, pricelist):
        self.ensure_one()
        context = self._get_product_price_context()
        context.update({'pricelist': pricelist.id})
        
        return pricelist._get_product_price(
            self.product_id.with_context(**context),
            self.product_uom_qty or 1.0,
            self.order_id.partner_id
        )
