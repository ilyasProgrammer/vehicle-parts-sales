# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger("# " + __name__)
_logger.setLevel(logging.DEBUG)


class FleetPartsAPI(http.Controller):

    @http.route('/web/load_part', type='http',  auth="public", csrf=False, website=True)
    def load_part(self, uid, db, vin, hash, data):
        # Add product.product
        product = self.env['product.product']
        if not data:
            return
        for r in data['result']:
            found = product.search([('c_id', '=', r['id'])])
            if not found:
                product.create(r)
                _logger.info("New product created: %s", r['name'])
            else:
                found[0].write(r)
                _logger.info("Old product found and updated: %s", r['name'])
        for r in data['result']['part']:
            found = product.search([('c_id', '=', r['id'])])
            if not found:
                product.create(r)
                _logger.info("New product created: %s", r['name'])
            else:
                found[0].write(r)
                _logger.info("Old product found and updated: %s", r['name'])

        return '{"response": "OK"}'

    @http.route('/web/load_part_image', type='http',  auth="public", csrf=False, website=True)
    def load_part_image(self, uid, db, vin, hash, data):
        # Add product.product
        product = self.env['product.product']
        if not data:
            return
        for r in data['result']:
            found = product.search([('c_id', '=', r['id'])])
            if not found:
                product.create(r)
                _logger.info("New product created: %s", r['name'])
            else:
                found[0].write(r)
                _logger.info("Old product found and updated: %s", r['name'])
        for r in data['result']['part']:
            found = product.search([('c_id', '=', r['id'])])
            if not found:
                product.create(r)
                _logger.info("New product created: %s", r['name'])
            else:
                found[0].write(r)
                _logger.info("Old product found and updated: %s", r['name'])

        return '{"response": "OK"}'

    @http.route('/web/delete_part', type='http',  auth="public", csrf=False, website=True)
    def delete_part(self, uid, db, vin, hash, data):
        # Add product.product
        product = self.env['product.product']
        if not data:
            return
        for r in data['result']:
            found = product.search([('c_id', '=', r['id'])])
            if not found:
                product.create(r)
                _logger.info("New product created: %s", r['name'])
            else:
                found[0].write(r)
                _logger.info("Old product found and updated: %s", r['name'])
        for r in data['result']['part']:
            found = product.search([('c_id', '=', r['id'])])
            if not found:
                product.create(r)
                _logger.info("New product created: %s", r['name'])
            else:
                found[0].write(r)
                _logger.info("Old product found and updated: %s", r['name'])

        return '{"response": "OK"}'