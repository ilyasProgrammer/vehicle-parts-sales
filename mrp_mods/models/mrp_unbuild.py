# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MrpUnbuildMod(models.Model):
    _inherit = "mrp.unbuild"

    product_qty = fields.Float('Quantity', default=1, required=True, states={'done': [('readonly', True)]})
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot',
        domain="[('product_id', '=', product_id)]",
        required=True,
        states={'done': [('readonly', True)]})


