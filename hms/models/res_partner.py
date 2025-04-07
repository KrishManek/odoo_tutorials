from odoo import fields,models,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    extra_discount = fields.Float(string="Extra Discount")
    
    terms_and_conditions = fields.Text(string="Terms and Conditions")
    use_customers_tc = fields.Boolean(string="Use Customer's Terms & Conditions", default=False)

    @api.model
    def write(self, vals):
        if self.env.context.get('from_patient_write'):
            return super().write(vals)
        res = super().write(vals)
        data=self.env['patient.details'].search([('partner_id','=',self.id)])
        for rec in data:
            rec.with_context(from_partner_write=True).write({
                'email':self.email,
                'phone':self.phone
                })
        return res