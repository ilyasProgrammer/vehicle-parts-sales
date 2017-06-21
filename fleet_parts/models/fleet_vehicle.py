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

    part_line_ids = fields.One2many('fleet.part.line', 'vehicle_id', string=u'Детали')
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

    c_id = fields.Integer('АйДи каталога')
    note = fields.Char(u'Примечание')
    oem = fields.Char(u'Артикул')
    secondOem = fields.Char(u'GMNUM артикул')


class PartLine(models.Model):
    _name = "fleet.part.line"
    _description = u'Строка таблицы товаров разборщика'

    vehicle_id = fields.Many2one('fleet.vehicle', string=u'Авто')
    product_id = fields.Many2one('product.product', string=u'Деталь')
    guid = fields.Char(u'АйДи')
    type = fields.Selection([('ORIGINAL','ORIGINAL'), ('NONORIGINAL','NONORIGINAL'), ('REUSED','REUSED')], default='ORIGINAL')
    rate = fields.Integer(u'Состояние')
    price = fields.Float(u'Цена')
    sellingRate = fields.Integer(u'Продаваемость')
    weight = fields.Float(u'Вес')
    volume = fields.Float(u'Объем')


class VehicleBrand(models.Model):
    _inherit = "fleet.vehicle.model.brand"

    c_id = fields.Integer(u'ID каталога')
    code = fields.Char(u'Код')
    brand = fields.Char(u'Бренд')
    allowVinSearch = fields.Boolean(u'Разрешить поиск по каталогу')
    type = fields.Char(u'Тип')
    parentId = fields.Many2one('fleet.vehicle.model.brand')

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
                found = brand.search([('c_id', '=', int(r['id']))])
                if not found:
                    r['c_id'] = int(r['id'])
                    if r.get('parentId', False):
                        found_parent = brand.search([('c_id', '=', int(r['parentId']))])
                        if found_parent:
                            r['parentId'] = found_parent.id
                    new_brand = brand.create(r)
                    self._cr.commit()
                    _logger.info("New brand created: %s", new_brand.name)
                else:
                    found[0].write(r)
                    _logger.info("Old brand found and updated: %s", found.name)


class VehicleModel(models.Model):
    _inherit = "fleet.vehicle.model"

    c_id = fields.Integer(u'ID каталога')
    modelCode = fields.Char(u'Код модели')

    @api.model
    def sync_models(self):
        # called by cron
        url = 'http://develop.itbrat.ru:8080/krafto-crawler/frontend/modelsinfo.jsp?uid=0&db=demo&fleet_id=0&vin=WVWZZZ3BZVP098238&hash=86DEF2B13F7C128462625C239F62055F'
        req = urllib2.Request(url)
        brand = self.env['fleet.vehicle.model.brand']
        model = self.env['fleet.vehicle.model']
        try:
            response = urllib2.urlopen(req, timeout=20)
        except urllib2.URLError, e:
            raise TimeOut("There was an error: %r" % e)
        if response:
            data = json.load(response)
            for r in data['result']:
                found = model.search([('c_id', '=', int(r['id']))])
                if not found:
                    found_brand = brand.search([('c_id', '=', int(r['brandId']))])
                    r['brand_id'] = found_brand.id
                    r['c_id'] = int(r['id'])
                    model.create(r)
                    self._cr.commit()
                    _logger.info("New model created: %s", r['name'])
                else:
                    found[0].write(r)
                    _logger.info("Old model found and updated: %s", r['name'])
