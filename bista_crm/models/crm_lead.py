from odoo import fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    
    product_ids = fields.Many2many('product.product', string="Products")
    probability_stage = fields.Many2one('probability.stage', string="Probability Stage")
    
    
    def _prepare_opportunity_quotation_context(self):
        res = super(CrmLead,self)._prepare_opportunity_quotation_context()
        order_lines =[]
        for product in self.product_ids:
            order_lines.append((0, 0, {'product_id': product.id,
                                       'product_uom_qty':1,}))
        res.update({'default_order_line': order_lines})
        if self.probability_stage:
            res.update({'default_probability_stage':self.probability_stage.id})
        return res