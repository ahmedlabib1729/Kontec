# See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.tools import format_datetime


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    date_approve = fields.Datetime(related="order_id.date_approve", store=True)
    # Added New field #T6893
    display_purchase_widget = fields.Boolean(compute="_compute_purchase_history")

    def purchase_order_history(self):
        """T4975 returns the information that will be used in popover."""

        purchase_order_line = []
        if not self.product_id:
            return purchase_order_line
        order_line = self.env["purchase.order.line"].search(
            [
                ("order_id", "!=", self.order_id.id),
                ("product_id", "=", self.product_id.id),
                ("state", "in", ("done", "purchase")),
            ],
            limit=10,
            order="date_approve desc",
        )

        for line in order_line:
            purchase_order_line.append(
                {
                    "vendor_name": line.order_id.partner_id.name,
                    "date_of_purchase": format_datetime(self.env, line.date_approve),
                    "price_unit": line.price_unit,
                    "product_qty": line.product_qty,
                }
            )

        return purchase_order_line

    def _compute_purchase_history(self):
        """New compute method to set the value of display_purchase_widget field
        based on the po line records.#T6893"""
        for line in self:
            order_line = line.env["purchase.order.line"].search(
                [
                    ("order_id", "!=", line.order_id.id),
                    ("product_id", "=", line.product_id.id),
                    ("state", "in", ("done", "purchase")),
                ],
                limit=1,
            )
            if not order_line:
                line.display_purchase_widget = False
                continue
            line.display_purchase_widget = True
