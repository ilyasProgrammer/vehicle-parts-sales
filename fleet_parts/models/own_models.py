# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions
import logging

_logger = logging.getLogger("# " + __name__)
_logger.setLevel(logging.DEBUG)


class PartLine(models.Model):
    _name = "fleet.part.line"
    _description = u'Строка таблицы товаров разборщика'

    vehicle_id = fields.Many2one('fleet.vehicle', string=u'Авто')
    product_id = fields.Many2one('product.product', string=u'Деталь')
    guid = fields.Char(u'ID')
    type = fields.Selection([('ORIGINAL','ORIGINAL'), ('NONORIGINAL','NONORIGINAL'), ('REUSED','REUSED')], default='ORIGINAL')
    rate = fields.Integer(u'Состояние')
    price = fields.Float(u'Цена')
    sellingRate = fields.Integer(u'Продаваемость')
    weight = fields.Float(u'Вес')
    volume = fields.Float(u'Объем')
