from odoo import fields,models,api
from  datetime import date

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    """ def action_process_all(self):
        self.action_confirm()
        purchase = self._get_purchase_orders()
        if purchase:
            purchase.button_confirm()
            purchase.picking_ids.button_validate()
        self.picking_ids.action_confirm()
        self.picking_ids.action_assign()
        self.picking_ids.button_validate()
        self._create_invoices()
        self.invoice_ids.action_post()
        invoice = self.invoice_ids.action_register_payment()
        act_ids = invoice['context']['active_ids']
        wizard = self.env['account.payment.register'].with_context(active_model='account.move.line', active_ids=act_ids).create({})
        wizard.action_create_payments()
        self.order_line.purchase_line_ids.order_id """
        
    def action_process_all(self):
        self.action_confirm()
        po = self._get_purchase_orders()
        if po:
            po.button_confirm()
            for order in po:
                for line in order.order_line:
                    for move in line.move_ids:
                        for line in self.order_line:
                            if line.product_id.id == move.product_id.id:
                                move.quantity = line.process_qty
                                break
        po.action_view_picking()
        data = po.picking_ids.button_validate()
        if data != True:
            context = data.get('context')
            picking = context.get('button_validate_picking_ids')
            pickings_to_validate = self.env['stock.picking'].browse(picking).with_context(skip_backorder=True)
            pickings_to_validate.button_validate()
            
        # po.action_create_invoice()
        # invoice_ids = po.invoice_ids
        # invoice_ids.update({'invoice_date': date.today()})
        # po.invoice_ids.action_post()
        # self.picking_ids.action_assign()
                
        for order in self:
            for line in order.order_line:
                for move in line.move_ids:
                    move.quantity = line.process_qty
                    
        # self.picking_ids.button_validate()            
        data = self.picking_ids.button_validate()
        context = data.get('context')
        picking = context.get('button_validate_picking_ids')
        # pickings_to_validate = self.env.context.get('button_validate_picking_ids')
        pickings_to_validate = self.env['stock.picking'].browse(picking).with_context(skip_backorder=True)
        pickings_to_validate.button_validate()
        
        
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        for move in self.move_ids:
            if move.state not in ['done','cancel']:
                move.quantity = self.process_qty
        for purchase in self.purchase_line_ids:
            if purchase.state in ['draft','sent','to_approve']:
                purchase.qty_recived = self.process_qty
        return res