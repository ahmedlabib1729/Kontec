{
    'name': 'Product weight in purchase Order',
    'version': '18.0',
    'category': 'Purchase',
    'summary': 'Total Weight of the Purchase Order Products,Display product weight in Purchase Order RFQs and print weight details on receipts for efficient product handling and tracking.',
    'description': """
The Product Weight in Purchase Order app for Odoo allows users to view and manage product weight details in the Purchase Request for Quotation (RFQ) and display the weight information on receipts. This feature ensures better product handling and tracking during the purchasing process.

Key Features:
- Product Weight Display: Easily view product weight in the RFQ view, helping users track product specifications before confirming orders.
- Unit of Measurement (UOM): The app also displays the UOM for product weight, providing a more precise and standardized measurement.
- RFQ and Receipt Integration: Product weight information is displayed both in the RFQ and on the corresponding receipt, ensuring consistency in product details across different stages.
- Improved Product Tracking: Helps in logistics and inventory management by providing clear weight details for each product during the purchase process.

This app simplifies the tracking and management of product weights in the purchase order workflow, streamlining processes from quotation to receipt. It’s an essential tool for businesses looking to ensure accurate weight data is displayed and printed in all relevant documents.
""",

    'author': 'INKERP',
    'website': 'www.inkerp.com',
    'depends': ['purchase'],

    'data': [
        'reports/purchase_quotation_template.xml',
        'reports/purchase_order_template.xml',
        'views/purchase_order_view.xml',
    ],
    
    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
