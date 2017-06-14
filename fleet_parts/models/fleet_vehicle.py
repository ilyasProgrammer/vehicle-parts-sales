# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
import json
import urllib2
import xml.etree.ElementTree
import base64
import re
from bs4 import BeautifulSoup as bs
import string

_logger = logging.getLogger("# " + __name__)
_logger.setLevel(logging.DEBUG)


class FleetVehicleParts(models.Model):
    _inherit = "fleet.vehicle"

    part_ids = fields.One2many('product.product', 'vehicle_id', string=u'Детали')

    @api.one
    def add_part(self):
        data = {
            'uid': self._context['uid'],  # int
            'db': self.env.cr.dbname,  # string
            'fleet_id': self.id  # int
        }

        req = urllib2.Request('http://example.com/api/posts/create')
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps(data))
        return True


class ProductVehicle(models.Model):
    _inherit = "product.product"

    vehicle_id = fields.Many2one('product.product', 'fleet')


