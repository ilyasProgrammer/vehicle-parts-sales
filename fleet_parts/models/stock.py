# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions
import logging
import json
import urllib2
import hashlib
from odoo.tools.translate import _

_logger = logging.getLogger("# " + __name__)
_logger.setLevel(logging.DEBUG)


class StockPickingMod(models.Model):
    _inherit = "stock.picking"

    vehicle_id = fields.Many2one('fleet.vehicle', string=u'Авто')
