# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Stock Card Report",
    "depends": [
        'base_setup',
        'web', 
        'stock',
        ],
    "application": True,
    "data": [
        'security/stock_card_groups.xml',
        'security/ir.model.access.csv',
        'report/stock_card_report_templates.xml',
        'report/stock_card_reports.xml',
        'wizard/stock_card_report_wizard_views.xml',
    ],

    "auto_install": False,
    "installable": True,
}
