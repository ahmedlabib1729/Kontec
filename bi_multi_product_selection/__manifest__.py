# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    "name" : "Multi Product Selection in Sales & Purchase",
    "version" : "18.0.0.0",
    "category" : "Extra Tools",
    "summary": 'Multiple product selection sales multi products selection purchase select multiple products on delivery order line add multiple products invoice line sales order add multi products purchase order multi product selection sales and purchase multiple products',
    "description": """ 

        Multi Product Selection Odoo App helps users to select multiple product in sales order line, purchase order line, delivery order line and an invoice line. User can add multiple product in order line with single click and only in draft stage.

    """,
    "author": "BROWSEINFO",
    "website" : "https://www.browseinfo.com/demo-request?app=bi_multi_product_selection&version=18&edition=Community",
    "depends" : ['base','sale_management','purchase','stock'],
    "data": [
            'security/ir.model.access.csv',
            'views/sale_order_view.xml',
            'views/purchase_order_view.xml',
            'views/account_move_view.xml',
            'views/stock_picking_view.xml',
            'wizard/purchase_order_wizard_view.xml',
            'wizard/sale_order_wizard_view.xml',
            'wizard/account_move_wizard_view.xml',
            'wizard/stock_picking_view.xml',
            ],
    'license':'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://www.browseinfo.com/demo-request?app=bi_multi_product_selection&version=18&edition=Community',
    "images":['static/description/Banner.gif'],
}
