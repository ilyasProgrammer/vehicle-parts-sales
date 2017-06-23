# -*- coding: utf-8 -*-

from odoo import http, api, registry
from odoo.http import request
import json
import logging

_logger = logging.getLogger("# " + __name__)
_logger.setLevel(logging.DEBUG)


class FleetPartsAPI(http.Controller):

    @http.route('/web/load_part', type='http',  auth="public", csrf=False, website=True)
    def load_part(self, uid, db, vin, hash, data):
        # Add product.product
        # TODO создавать от имени юзера а не судо
        product = request.env['product.product']
        line = request.env['fleet.part.line']
        car = request.env['fleet.vehicle']
        if not data:
            return
        data = json.loads(data)
        found = product.sudo().search([('c_id', '=', data['part']['id'])])
        if not found:
            data['part']['c_id'] = data['part']['id']
            new_product = product.sudo().create(data['part'])
            _logger.info("New product created: %s", new_product.name)
        else:
            found[0].sudo().write(data['part'])
            new_product = found[0]
            _logger.info("Old product found and updated: %s", data['part']['name'])
        request.cr.commit()
        found_line = line.sudo().search([('guid', '=', data['guid'])])
        if not found_line:
            car_to_add_line = car.sudo().search([('vin_sn', '=', vin)])
            vals = {'c_id': data['id'],
                    'product_id': new_product.id,
                    'guid': data['guid'],
                    'partId': data['partId'],
                    'amount': data['amount'],
                    }
            if data.get('type', False):
                vals['type'] = data['type']
            if data.get('rate', False):
                vals['rate'] = data['rate']
            if data.get('price', False):
                vals['price'] = data['price']
            if data.get('description', False):
                vals['description'] = data['description']
            if data.get('sellingRate', False):
                vals['sellingRate'] = data['sellingRate']
            if data.get('weight', False):
                vals['weight'] = data['weight']
            if data.get('volume', False):
                vals['volume'] = data['volume']
            if car_to_add_line:
                vals['vehicle_id'] = car_to_add_line.id
            line.sudo().create(vals)
            _logger.info("New sale item created: %s", data['guid'])
        else:
            found_line[0].sudo().write(data)
            _logger.info("Old sale item found and updated: %s", data['name'])

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