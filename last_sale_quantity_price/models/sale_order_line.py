from odoo import models, fields, api, _




class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    last_purchase_qty = fields.Float(string="Last Quantity", compute="_compute_last_purchase_qty_price")
    last_purchase_price = fields.Float(string="Last Price", compute="_compute_last_purchase_qty_price")
    free_qty = fields.Float(related='product_id.free_qty')

    def _compute_last_purchase_qty_price(self):
        for so_line_id in self:
            so_line_id.last_purchase_qty = 0
            so_line_id.last_purchase_price = 0
            if type(so_line_id.id) == int:
                last_po_line_id = self.search(
                    [('product_id', '=', so_line_id.product_id.id),
                     ('order_partner_id', '=', so_line_id.order_partner_id.id),
                     ('id', '!=', so_line_id.id)],
                    order='id desc', limit=1)
            else:
                last_po_line_id = self.search(
                    [('product_id', '=', so_line_id.product_id.id),
                     ('order_partner_id', '=', so_line_id.order_partner_id.id),
                     ('id', '!=', so_line_id.id.origin)],
                    order='id desc', limit=1)

            if last_po_line_id:
                so_line_id.last_purchase_qty = last_po_line_id.product_uom_qty
                so_line_id.last_purchase_price = last_po_line_id.price_unit
