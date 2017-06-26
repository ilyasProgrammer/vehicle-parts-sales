# -*- coding: utf-8 -*-
{
    'name': "fleet_parts",
    'description': """fleet_parts""",
    'summary': """fleet_parts""",
    'author': "Ilyas",
    'website': "https://github.com/ilyasProgrammer",
    'category': 'Custom',
    'version': '1.0',
    'depends': [
        'sale',
        'fleet',
        'stock',
                ],
    'data': [
        'views/fleet_vehicle.xml',
        'views/parts.xml',
        'views/stock.xml',
        'cron_jobs.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
