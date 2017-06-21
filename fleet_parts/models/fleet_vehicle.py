# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
import json
import urllib2
import hashlib

_logger = logging.getLogger("# " + __name__)
_logger.setLevel(logging.DEBUG)


class TimeOut(Exception):
    pass


class FleetVehicleParts(models.Model):
    _inherit = "fleet.vehicle"

    part_ids = fields.One2many('product.product', 'vehicle_id', string=u'Детали')
    vin = fields.Char(string=u'ВИН', default='WAUZZZ8ZZ1N006767')

    @api.multi
    def add_part(self):
        args = str(self._context['uid']) + self.env.cr.dbname + str(self.id) + self.vin
        key = 'test'
        data = hashlib.md5(args + key)
        url = 'http://develop.itbrat.ru:8080/krafto-crawler/frontend/razbor.jsp?uid=%s&db=%s&fleet_id=%s&vin=%s&hash=%s'
        data_hash = data.hexdigest()
        url_arg = (self._context['uid'], self.env.cr.dbname, self.id, self.vin, data_hash)
        return {
            'type': 'ir.actions.act_url',
            'url': url % url_arg,
            'target': 'self',
        }

    @api.one
    def get_price(self):
        data = {
            'uid': self._context['uid'],  # int
            'db': self.env.cr.dbname,  # string
            'fleet_id': self.id  # int
        }
        data = {"id":123,"method":"parts.prices","params": {"ident":"8e0201803l"},"jsonrpc":"2.0"}
        req = urllib2.Request('http://172.16.4.202')
        req.add_header('Content-Type', 'application/json')

        try:
            response = urllib2.urlopen(req, json.dumps(data), timeout=20)
        except urllib2.URLError, e:
            raise TimeOut("There was an error: %r" % e)
        return True


class ProductVehicle(models.Model):
    _inherit = "product.product"

    vehicle_id = fields.Many2one('product.product', 'fleet')
    guid = fields.Char(u'АйДи')
    type = fields.Selection([('ORIGINAL'), ('NONORIGINAL'), ('REUSED')])
    rate = fields.Integer(u'Состояние')
    sellingRate = fields.Integer(u'Продаваемость')
    note = fields.Char(u'Примечание')
    oem = fields.Char(u'Артикул')
    secondOem = fields.Char(u'GMNUM артикул')


class VehicleBrand(models.Model):
    _inherit = "fleet.vehicle.model.brand"

    c_id = fields.Integer('АйДи каталога')
    code = fields.Char(u'Код')
    brand = fields.Char(u'Бренд')
    allowVinSearch = fields.Boolean(u'Разрешить поиск по каталогу')
    type = fields.Char(u'Тип')
    parentId = fields.Integer(u'АйДи родителя')

    @api.model
    def sync_brands(self):
        # called by cron
        url = 'http://develop.itbrat.ru:8080/krafto-crawler/frontend/catalogsinfo.jsp?uid=0&db=demo&fleet_id=0&vin=WVWZZZ3BZVP098238&hash=86DEF2B13F7C128462625C239F62055F'
        req = urllib2.Request(url)
        brand = self.env['fleet.vehicle.model.brand']
        try:
            response = urllib2.urlopen(req, timeout=20)
        except urllib2.URLError, e:
            raise TimeOut("There was an error: %r" % e)
        if response:
            data = json.load(response)
            for r in data['result']:
                found = brand.search([('name', '=', r['name'])])
                if not found:
                    brand.create(r)
                    _logger.info("New brand created: %s", r['name'])
                else:
                    found[0].write(r)
                    _logger.info("Old brand found and updated: %s", r['name'])
