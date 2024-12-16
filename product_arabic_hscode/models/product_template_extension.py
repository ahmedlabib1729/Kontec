from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_name_ar = fields.Char(string="اسم المنتج بالعربي", help="Arabic name of the product")
    hs_code = fields.Char(string="HS Code", help="Harmonized System Code for the product")
