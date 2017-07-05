# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions
import logging
import json
import urllib2
import hashlib
from odoo.tools.translate import _

_logger = logging.getLogger("# " + __name__)
_logger.setLevel(logging.DEBUG)


class ProductVehicle(models.Model):
    _inherit = "product.template"

    c_id = fields.Integer('АйДи каталога')
    brandId = fields.Integer('brandId')
    note = fields.Char(u'Примечание')
    oem = fields.Char(u'Артикул')
    secondOem = fields.Char(u'GMNUM артикул')
    price_ids = fields.One2many('fleet.part.price', 'product_id')

