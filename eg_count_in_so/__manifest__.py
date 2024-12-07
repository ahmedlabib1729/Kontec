{
    'name': 'Item Count In Sale Order',
    'version': '18.0',
    'category': 'Sale',
     'summary': 'Track total item quantities in sale orders, including ordered, invoiced, and delivered quantities.item count sale order, track item quantities, ordered quantity tracking, invoiced quantity tracking, delivered quantity tracking, sale order management, sales tracking, inventory tracking, sale order documentation, quotation print PDF, Odoo sales module, total item count, sales process efficiency, stock management, sale order analytics, sales and inventory integration, streamline sales processes, order status tracking, sale order automation, Odoo customization',
    'description': """
        The Item Count in Sale Order app allows users to track the total quantity of items in a sale order. It shows the ordered quantity, the invoiced quantity, and the delivered quantity, helping sales and inventory teams keep track of the status of sale orders. These quantities are also displayed in the Quotation Print PDF for clear documentation.
    """,
    'author': 'INKERP',
    'website': 'http://www.inkerp.com',
    'depends': ['sale_management', 'stock'],
    
    'data': [
        'views/sale_order_view.xml',
        'report/sale_order_report.xml',
    ],
    
    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
