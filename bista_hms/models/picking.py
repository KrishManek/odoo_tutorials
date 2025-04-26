from odoo import models, api, fields
from odoo.api import depends


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    lead_referral = fields.Char(related='sale_id.lead_reference',
                                depends=['sale_id.lead_reference'],
                                string='Lead Referral', store=True)


