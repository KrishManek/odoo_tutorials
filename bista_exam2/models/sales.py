from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_service_products = fields.Integer(string="Service Products", compute="compute_total_service_products", store=True)
    state = fields.Selection(selection_add=[('to_approve', 'To approve'), ('sale', '')])
    
    @api.depends('order_line.product_id')
    def compute_total_service_products(self):
        service_prod = 0
        for product in self.order_line:
            if product.product_id.type =='service':
                service_prod += 1
        self.total_service_products = service_prod
    def action_open_add_product_wizard(self):
        veiw_id = self.env.ref("bista_exam2.view_sale_wizard_form").id
        return {
            'name' : "Add Products Window",
            'view_mode' : "form",
            'res_model' : 'sale.wizard',
            'view_id' : veiw_id,
            'type' : "ir.actions.act_window",
            'target' : 'new',
            'context': {'default_sale_id': self.id}
        }
    def button_approve(self, force=False):
        orders = self.filtered(lambda order: order._allowed() and order.state in ['draft', 'sent', 'to_approve'])
        if orders:
            super(SaleOrder, orders).action_confirm()

    def _confirmation_error_message(self):
        self.ensure_one()
        
        if self.state not in {'draft', 'sent', 'to_approve'}:
            return("Some orders are not in a state requiring confirmation.")

        if any(
            not line.display_type
            and not line.is_downpayment
            and not line.product_id
            for line in self.order_line
        ):
            return("A line on these orders is missing a product, you cannot confirm it.")

        return False

    def _allowed(self):
        self.ensure_one()
        sale_min_amount = float(self.env['ir.config_parameter'].sudo().get_param('bista_exam2.sale_min_amount'))
        if sale_min_amount < self.amount_total and self.env.user.has_group('bista_exam2.group_sale_approver'):
            return True
        elif self.env.user.has_group('bista_exam2.group_sale_approver'):
            return True
            
    def action_confirm(self):
        for order in self:
            if order._allowed():
                order.button_approve()
            else:
                order.write({'state': 'to_approve'})