# See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.tools import format_datetime


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_order = fields.Datetime(related="order_id.date_order", store=True)
    # Added New field #T6892
    display_sale_widget = fields.Boolean(compute="_compute_sale_history")

    def sale_order_history(self):
        """T4976 returns required information that will be used in popover."""
        sale_order_line = []
        if not self.product_id:
            return sale_order_line
        order_line = self.env["sale.order.line"].search(
            [
                ("id", "not in", self.order_id.order_line.ids),
                ("product_id", "=", self.product_id.id),
                ("state", "=", "sale"),
            ],
            limit=10,
            order="date_order desc",
        )
        for line in order_line:
            sale_order_line.append(
                {
                    "customer_name": line.order_id.partner_id.name,
                    "date_of_sale": format_datetime(self.env, line.date_order),
                    "price_unit": line.price_unit,
                    "product_qty": line.product_uom_qty,
                }
            )
        return sale_order_line

    def _compute_sale_history(self):
        """New compute method to set the value of display_sale_widget field
        based on the so line records.#T6892"""
        for line in self:
            order_line = line.env["sale.order.line"].search(
                [
                    ("order_id", "!=", line.order_id.id),
                    ("product_id", "=", line.product_id.id),
                    ("state", "=", "sale"),
                ],
                limit=1,
            )
            if not order_line:
                line.display_sale_widget = False
                continue
            line.display_sale_widget = True
