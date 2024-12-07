from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    total_weight = fields.Float(string='Total Product Weight', compute='_compute_total_weight')

    @api.depends('order_line.product_id', 'order_line.product_qty')
    def _compute_total_weight(self):
        for record in self:
            product_total_weight = 0
            for order_line_id in record.order_line:
                product_total_weight += order_line_id.product_weight
            record.total_weight = product_total_weight
