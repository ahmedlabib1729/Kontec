
{
    "name": "Sale Order Automatic Workflow ",

    "author": "Keroles Ayed",

    "license": "OPL-1",



    "depends": ["sale_management", "stock",'purchase'],
    "data": [

        'security/ir.model.access.csv',
        'security/sh_sale_workflow_groups.xml',
        'views/res_config_settings_views.xml',
        'views/sh_auto_sale_workflow_views.xml',
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',

    ],
    "auto_install": False,
    "installable": True,
    "application": True,
}
