from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_weight = fields.Float(string='Product Weight', compute='_compute_product_weight')

    @api.depends('product_id', 'product_qty')
    def _compute_product_weight(self):
        for record in self:
            record.product_weight = (record.product_id.weight * record.product_qty)
