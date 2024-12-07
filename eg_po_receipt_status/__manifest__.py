{
    'name': 'Receipt Status on Purchase order',
    'version': '18.0',
    'category': 'Sale',
    'summary': 'Track and manage the receipt status of purchase orders, ensuring smooth procurement processes and accurate inventory management in Odoo.',
    'description': """
    The eg_po_receipt_status app for Odoo allows users to track and manage the receipt status of purchase orders (POs), ensuring smooth procurement processes and accurate inventory management. This app provides visibility into the status of goods received, enabling users to easily monitor which orders have been fully received, partially received, or are yet to be received.

    With this feature, businesses can streamline their purchasing process, maintain better control over inventory levels, and prevent delays in the supply chain. It enhances the efficiency of procurement teams by providing real-time data on receipt status, helping them make better decisions regarding stock management and payment processing.

    Key Features:
    - Track Receipt Status: Easily track the status of goods received for each purchase order (fully received, partially received, or not yet received).
    - Improved Procurement Efficiency: Provides real-time updates on PO receipt status, ensuring procurement teams stay informed throughout the process.
    - Accurate Inventory Management: Helps maintain accurate inventory records by aligning purchase order receipts with actual stock levels.
    - Enhanced Communication: Facilitates better coordination between procurement and inventory teams, ensuring timely order fulfillment and reducing errors.
    - Seamless Integration with Odoo: Integrates smoothly with the Odoo procurement and inventory modules to provide a unified system for managing orders and receipts.

    The eg_po_receipt_status app is ideal for businesses looking to streamline their purchasing and inventory management processes. By providing clear visibility into the receipt status of each purchase order, this app ensures that companies can effectively manage their supply chain, track inventory levels, and prevent stock-related issues or delays.
    """,
    'author': 'INKERP',
    'website': "https://www.inkerp.com",
    'depends': ['purchase', 'purchase_stock'],

    'data': [
        'views/purchase_order_view.xml',
    ],

    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
