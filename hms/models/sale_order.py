from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    lead_reference = fields.Char(string="Lead Reference")
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            partner_id = vals.get('partner_id')
            if partner_id:
                partner = self.env['res.partner'].browse(partner_id)
                if partner.use_customers_tc and partner.terms_and_conditions:
                    vals['note'] = partner.terms_and_conditions
        return super(SaleOrder, self).create(vals_list)
