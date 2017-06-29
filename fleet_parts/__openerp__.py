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
        'website',
        'website_sale',
                ],
    'data': [
        'views/fleet_vehicle.xml',
        'views/parts.xml',
        'views/stock.xml',
        'views/product.xml',
        'cron_jobs.xml',
        'views/templates.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
