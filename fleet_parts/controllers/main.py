# -*- coding: utf-8 -*-

from odoo import http
import json
from odoo.http import request
from odoo.tools import ustr
from odoo.tools.misc import xlwt


class FleetPartsAPI(http.Controller):

    @http.route('/web/load_part', type='json',  auth="none", methods=['POST'], csrf=False)
    def load_part(self, uid, db, vehicle_id, vin, hash, data):
        print 'OK VERY GOOD'
