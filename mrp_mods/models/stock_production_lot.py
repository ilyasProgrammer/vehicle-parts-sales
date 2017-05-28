# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    @api.model
    def default_get(self, fields):
        res = super(StockProductionLot, self).default_get(fields)
        ctx = self.env.context
        product_id = ctx.get('product_id', False)
        if product_id:
            res['product_id'] = product_id
        lot_id = ctx.get('lot_id', False)
        if lot_id:
            res['ref'] = self.env['stock.production.lot'].browse(lot_id).name
        return res

    @api.model
    def create(self, vals):
        vals['ref'] = vals['name']
        res = super(StockProductionLot, self).create(vals)
        return res