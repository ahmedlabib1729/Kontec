from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    order_quantity = fields.Float(string="No. Ordered Quantity", compute='_compute_total_quantity')
    deliver_quantity = fields.Float(string="No. Delivered Quantity", compute='_compute_total_quantity')
    invoice_quantity = fields.Float(string="No. Invoiced Quantity", compute='_compute_total_quantity')

    def _compute_total_quantity(self):
        for sale_order in self:
            sale_order.order_quantity = sum(sale_order.order_line.mapped('product_uom_qty'))
            sale_order.deliver_quantity = sum(sale_order.order_line.mapped('qty_delivered'))
            sale_order.invoice_quantity = sum(sale_order.order_line.mapped('qty_invoiced'))
