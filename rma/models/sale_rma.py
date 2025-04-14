from odoo import fields, models, api
from odoo.exceptions import ValidationError,UserError


class SaleRMA(models.Model):
    _name = "sale.rma"
    _description = "Sale RMA"


    name = fields.Char(string="RMA Reference", required=True, copy=False, readonly=True, default="New")
    date = fields.Date(default=fields.Date.today, string="Date")
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    team_id = fields.Many2one('rma.team', string="Team", required=True)
    line_ids = fields.One2many('sale.rma.line', 'rma_id', string="RMA Lines")
    picking_ids = fields.One2many("stock.picking", 'rma_id', string="Sale RMA IDs")
    delivery_count = fields.Integer(compute="_compute_delivery_count", string="Delivery Count", store=True)
    rma_created = fields.Boolean(string="Order created", default=False)
        
    
    @api.depends('picking_ids')
    def _compute_delivery_count(self):
        for delivery in self:
            delivery.delivery_count = self.env['stock.picking'].search_count([('rma_id', '=', delivery.id)])
            
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New' and vals.get('team_id'):
                team = self.env['rma.team'].browse(vals['team_id'])
                seq_code = f'rma.team.{team.id}'
                vals['name'] = self.env['ir.sequence'].next_by_code(seq_code) or 'New'
            vals['rma_created'] = True
        return super().create(vals_list)


    @api.onchange('sale_order_id')
    def _onchange_sale_order_id(self):
        if self.sale_order_id:
            self.line_ids = [(5, 0, 0)] 
            lines = []
            for line in self.sale_order_id.order_line:
                lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'so_qty': line.product_uom_qty,
                    'unit_price': line.price_unit,
                    'to_receive': line.product_uom_qty,
                    
                }))
            self.line_ids = lines
            
    def action_open_wizard(self):
        veiw_id = self.env.ref("rma.view_rma_wizard").id
        return {
            'name' : "return Window",
            'view_mode' : "form",
            'res_model' : 'rma.wizard',
            'view_id' : veiw_id,
            'type' : "ir.actions.act_window",
            'target' : 'new',
            'context': {'default_act_id': self.id}
        }
        
    def action_open_delivery(self):
        form_view_id = self.env.ref('stock.view_picking_form').id  # Get form view ID
        list_view_id = self.env.ref('stock.vpicktree').id  # Get list view ID

        res = {
            'name': 'Stock Picking',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'target': 'current',
            'domain': [('rma_id', '=', self.id)],
            'views':[(list_view_id, 'list'), (form_view_id, 'form')],
            'view_mode': 'list,form'   
        }
        return res
    
    def write(self, vals):
        for record in self:
            if record.sale_order_id and 'sale_order_id' in vals:
                raise UserError("Once order is created you can't change the Sale Order.")
        res = super().write(vals)
        return res 
    
    def write(self, vals):
        for record in self:
            if record.rma_created and 'sale_order_id' in vals:
                raise UserError("Once order is created you can't change the Sale Order.")
        res = super().write(vals)
        return res   
    
