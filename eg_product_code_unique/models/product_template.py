from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.constrains("default_code")
    def _constraint_unique_default_code_product_template(self):
        for rec in self:
            if rec.default_code:
                product_id = self.env["product.template"].search(
                    [("id", "!=", rec.id), ("default_code", "=", rec.default_code)])
                if product_id:
                    raise ValidationError(
                        "Product with \"{}\" internal reference already exist!!!".format(product_id.default_code))
