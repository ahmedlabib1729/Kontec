{
    'name': 'Unique Code in Product',
    'version': '18.0',
    'category': 'Product',
        'summary': """
    The Unique Code in Product app allows users to assign unique internal reference numbers to products, ensuring each product can be easily identified. The app also prevents duplicate reference numbers by providing an error or warning message when the same number is entered.
    """,
    'description': """
    The Unique Code in Product app streamlines product identification by assigning a unique internal reference number to each product. This ensures that products can be easily searched and distinguished by their reference number, improving product management.

    Key features of the app include:

    - Unique Internal Reference Numbe: Users can assign a unique reference number to each product. This feature allows easy identification and tracking of products based on their reference numbers.
      
    - Duplicate Reference Number Warning: If a user tries to enter a duplicate internal reference number for a product, the app will display an error or warning message to prevent duplicates, ensuring each product has a unique identifier.

    - Product View Integration: The product view displays the internal reference number field, where users can enter the reference number when creating a product, making it easy to manage and reference products.

    - Error Prevention: The app enhances data integrity by ensuring no two products share the same reference number, reducing the risk of errors in product management.

    This app is ideal for businesses that require precise and efficient product identification with unique internal reference numbers.
    """,

    'author': 'INKERP',
    'website': "http://www.inkerp.com/",
    'depends': ['sale_management'],
    
    'data': ['views/product_template_view.xml'],
    
    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
