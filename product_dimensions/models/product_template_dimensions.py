from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    length_cm = fields.Float(string="Length (cm)", help="Length of the product in centimeters")
    width_cm = fields.Float(string="Width (cm)", help="Width of the product in centimeters")
    height_cm = fields.Float(string="Height (cm)", help="Height of the product in centimeters")

    @api.depends('length_cm', 'width_cm', 'height_cm')
    def _compute_volume(self):
        for record in self:
            if all([record.length_cm, record.width_cm, record.height_cm]):
                record.volume = record.length_cm * record.width_cm * record.height_cm
            else:
                record.volume = 0.0
