# See LICENSE file for full copyright and licensing details.

{
    "name": "Product Purchase History",
    "version": "18.0.1.0.0",
    "category": "Purchase",
    "depends": ["purchase_stock"],
    "author": "BizzAppDev Systems Pvt. Ltd.",
    "license": "Other proprietary",
    "website": "http://www.bizzappdev.com",
    "data": ["views/purchase_views.xml", "views/purchase_history_pivot_view.xml"],
    "assets": {
        "web.assets_backend": [
            "bad_product_purchase_history/static/src/js/**/*",
            "bad_product_purchase_history/static/src/xml/**/*",
        ],
    },
    "installable": True,
    "images": ["images/purchase_history_popover.png"],
}
