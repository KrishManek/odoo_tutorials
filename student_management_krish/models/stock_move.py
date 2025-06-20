# -*- coding: utf-8 -*-

from odoo import models


class StockMoveLine(models.Model):
    _inherit = 'stock.move'
        
    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        """Overrides method by super calling to add lot id in stock move line from purhase order line

        Args:
            quantity (float, optional): Defaults to None.
            reserved_quant (float, optional): Defaults to None.

        Returns:
            dictonary: returns dictoanry for move line vals with lot name 
        """
        vals = super()._prepare_move_line_vals(quantity, reserved_quant)
        if self.purchase_line_id.lot_name:
            vals['lot_name'] = self.purchase_line_id.lot_name
        return vals