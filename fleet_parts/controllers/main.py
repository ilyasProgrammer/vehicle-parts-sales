# -*- coding: utf-8 -*-

from collections import deque
import json

from odoo import http
from odoo.http import request
from odoo.tools import ustr
from odoo.tools.misc import xlwt


class FleetPartsAPI(http.Controller):

    @http.route('/web/load_part', type='json', auth='none')
    def load_part(self, uid, db, fleet_id):
        return True
