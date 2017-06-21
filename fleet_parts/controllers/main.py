# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class FleetPartsAPI(http.Controller):

    @http.route('/web/load_part', type='http',  auth="public", csrf=False, website=True)
    def load_part(self, uid, db, vin, hash, data):
        print 'OK VERY GOOD'
        return '{"response": "OK"}'
