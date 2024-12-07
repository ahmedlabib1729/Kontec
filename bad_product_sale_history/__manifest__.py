# See LICENSE file for full copyright and licensing details.

{
    "name": "Product Sale History",
    "version": "18.0.1.0.0",
    "category": "Sale",
    "depends": ["sale_stock", "sale_management"],
    "author": "BizzAppDev Systems Pvt. Ltd.",
    "license": "Other proprietary",
    "website": "http://www.bizzappdev.com",
    "data": ["views/sale_views.xml", "views/sale_history_pivot_view.xml"],
    "assets": {
        "web.assets_backend": [
            "bad_product_sale_history/static/src/js/**/*",
            "bad_product_sale_history/static/src/xml/**/*",
        ],
    },
    "images": ["images/sale_history_popover.png"],
    "installable": True,
}
