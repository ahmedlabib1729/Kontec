from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'purchase.order'

    ordered_quantity = fields.Float(string="No. Ordered Quantity", compute='_compute_total_quantity')
    received_quantity = fields.Float(string="No. Received Quantity", compute='_compute_total_quantity')
    biled_quantity = fields.Float(string="No. Billed Quantity", compute='_compute_total_quantity')

    def _compute_total_quantity(self):
        for purchase_order in self:
            purchase_order.ordered_quantity = sum(purchase_order.order_line.mapped('product_qty'))
            purchase_order.received_quantity = sum(purchase_order.order_line.mapped('qty_received'))
            purchase_order.biled_quantity = sum(purchase_order.order_line.mapped('qty_invoiced'))
