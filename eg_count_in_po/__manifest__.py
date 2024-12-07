{
    'name': 'Item Count In Purchase Order',
    'version': '18.0',
    'category': 'Purchase',
      'summary': 'Track total item quantities in purchase orders, including ordered, billed, and delivered quantities. Track total item quantities in purchase orders, including ordered, billed, and delivered quantities.purchase order, item count, procurement management, inventory tracking, ordered quantity, billed quantity, delivered quantity, RFQ print, stock management, Odoo app',
    'description': """
        The Item Count in Purchase Order app allows users to track the total quantity of items in a purchase order. It shows the ordered quantity, the billed quantity, and the delivered quantity, helping inventory and procurement teams ensure accurate stock management. These quantities are also displayed in the RFQ print for easy reference.
    """,
    'author': 'INKERP',
    'website': "https://www.inkerp.com",
    'depends': ['purchase'],

    'data': [
        'views/purchase_order_view.xml',
        'report/purchase_order_report.xml',
    ],

    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
