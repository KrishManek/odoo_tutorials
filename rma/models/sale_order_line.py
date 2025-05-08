from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    child_warehouse_id = fields.Many2one('stock.location', string='Child Warehouse')
    
    def _get_procurement_group(self):
        self.ensure_one()
        if self.child_warehouse_id:
            domain = [
                ('sale_id', '=', self.order_id.id),
                ('child_warehouse_id', '=', self.child_warehouse_id.id),
            ]
            return self.env['procurement.group'].search(domain, limit=1)
        return self.order_id.procurement_group_id

    def _prepare_procurement_group_vals(self):
        self.ensure_one()
        if self.child_warehouse_id:
            return {
                'name': f"{self.order_id.name} - {self.child_warehouse_id.display_name}",
                'move_type': self.order_id.picking_policy,
                'sale_id': self.order_id.id,
                'partner_id': self.order_id.partner_shipping_id.id,
                'child_warehouse_id': self.child_warehouse_id.id,
            }
        return super(SaleOrderLine,self)._prepare_procurement_group_vals()
        
    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        if self.child_warehouse_id:
            self.ensure_one()
            values.update({
                'warehouse_id': self.order_id.warehouse_id,
                'child_warehouse_id': self.child_warehouse_id,
            })
        return values
