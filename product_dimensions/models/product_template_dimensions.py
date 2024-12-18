from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    length_cm = fields.Float(
        string="Length (cm)",
        help="Length of the product in centimeters",
        digits=(16, 10)  # دقة 10 خانات بعد العلامة العشرية
    )
    width_cm = fields.Float(
        string="Width (cm)",
        help="Width of the product in centimeters",
        digits=(16, 10)
    )
    height_cm = fields.Float(
        string="Height (cm)",
        help="Height of the product in centimeters",
        digits=(16, 10)
    )
    count = fields.Integer(
        string="Count",
        help="Number of units for volume calculation",
        default=1
    )
    calculated_volume = fields.Float(
        string="Calculated Volume (cm³)",
        readonly=True,
        help="Volume before division by count",
        digits=(16, 10)
    )

    @api.depends('length_cm', 'width_cm', 'height_cm', 'count')
    def _compute_volume(self):
        for record in self:
            if all([record.length_cm, record.width_cm, record.height_cm, record.count > 0]):
                # الحساب: الطول × العرض × الارتفاع
                total_volume = record.length_cm * record.width_cm * record.height_cm
                record.calculated_volume = total_volume  # القيمة قبل القسمة
                record.volume = total_volume / record.count  # القسمة على العدد
            else:
                record.calculated_volume = 0.0
                record.volume = 0.0
