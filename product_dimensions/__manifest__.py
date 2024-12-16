{
    'name': "Product Dimensions",
    'version': '1.1',
    'summary': "Add length, width, height, and update volume to Inventory tab",
    'description': """
        This module adds:
        - Length (cm)
        - Width (cm)
        - Height (cm)
        - Updates the default Volume field in the Inventory tab
    """,
    'author': "Your Name",
    'website': "https://yourwebsite.com",
    'category': 'Inventory',
    'depends': ['base', 'product'],
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
