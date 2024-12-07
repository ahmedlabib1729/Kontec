# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Back Order Status in Sales and Purchase',
    'version': '18.0.0.0',
    'category': 'Sales',
    'summary': 'Sales Back order status purchase back order status sale back order status back order status on sales order back order status on purchase order back order status sale backorder status sale order back order status show back order status on sales purchase',
    'description' :"""
       
       Back Order Status in odoo,
       Back Order Filter in odoo,
       Back Order on Sale Order in odoo,
       Back Order on Purchase Order in odoo,
       Track Back Order in odoo,

    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.com',
    'depends': ['sale_management', 'purchase', 'stock'],
    'data': [
        'views/inherited_sale_order_view.xml',
        'views/inherited_purchase_order_view.xml',
    ],
    'license':'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/1DpJvS-1Rzs',
    "images":["static/description/Banner.gif"],
}
