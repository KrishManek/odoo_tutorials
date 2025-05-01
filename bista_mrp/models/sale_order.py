from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_process_all(self):
        self.action_confirm()
        purchase = self._get_purchase_orders()
        purchase.button_confirm()
        purchase.picking_ids.button_validate()
        #purchase.action_view_picking()
        """ self.picking_ids.action_confirm()
        self.picking_ids.action_assign()
        self.picking_ids.button_validate()
        self._create_invoices()
        self.invoice_ids.action_post()
        invoice = self.invoice_ids.action_register_payment()
        act_ids = invoice['context']['active_ids']
        wizard = self.env['account.payment.register'].with_context(active_model='account.move.line', active_ids=act_ids).create({})
        wizard.action_create_payments()
        self.order_line.purchase_line_ids.order_id """