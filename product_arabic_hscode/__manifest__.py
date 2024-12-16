{
    'name': "Product Arabic Name & HS Code",
    'version': '1.0',
    'summary': "Adds Arabic product name and HS Code to product template",
    'description': """
        This module adds:
        - Arabic Name for the product
        - HS Code field to the product template
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
