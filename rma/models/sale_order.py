from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        print("Hello")
        if not args:
            args = []
        cus_id = self._context.get('rma_customer_sale_order')
        if cus_id:
            args += [('partner_id', '=', cus_id)]
        else:
            return super().name_search(name, args, operator=operator, limit=limit)
        orders = self.search_fetch(args, ['name'], limit=limit)
        return [(order.id, order.display_name) for order in orders.sudo()]
    
    @api.model
    def web_search_read(self, domain, specification, offset=0, limit=None, order=None, count_limit=None):
        cus_id = self._context.get('rma_customer_sale_order')
        if cus_id:
            domain += [('partner_id', '=', cus_id)]
        return super().web_search_read(domain, specification, offset=offset, limit=limit, order=order,
                                    count_limit=count_limit)