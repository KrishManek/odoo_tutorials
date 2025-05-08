from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    location_id = fields.Many2one('stock.location', string='Warehouse Location')
    
    def _get_procurement_group(self):
        self.ensure_one()
        if self.location_id:
            return self.env['procurement.group'].search([
                                                    ('sale_id', '=', self.order_id.id),
                                                    ('location_id', '=', self.location_id.id),
                                                ], limit=1)
        return self.order_id.procurement_group_id

    def _prepare_procurement_group_vals(self):
        values = super(SaleOrderLine,self)._prepare_procurement_group_vals()
        if self.location_id:
            self.ensure_one()
            values.update({
                'location_id': self.location_id.id,
            })
        return values
        
    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        if self.location_id:
            self.ensure_one()
            values.update({
                'location_id': self.location_id.id,       
            })
        return values
