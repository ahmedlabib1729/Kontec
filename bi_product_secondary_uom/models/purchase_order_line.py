# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    secondary_uom_id = fields.Many2one('uom.uom', compute='_quantity_secondary_compute', string="Secondary UOM", store=True)
    secondary_quantity = fields.Float('Secondary Qty', compute='_quantity_secondary_compute', digits='Product Unit of Measure', store=True)

    @api.depends('product_id', 'product_qty', 'product_uom')
    def _quantity_secondary_compute(self):
        for order in self:
            if order.product_id.secondary_uom:
                uom_quantity = order.product_id.uom_id._compute_quantity(order.product_uom_qty, order.product_id.secondary_uom_id, rounding_method='HALF-UP')
                order.update({'secondary_uom_id' : order.product_id.secondary_uom_id})
                order.update({'secondary_quantity' : uom_quantity})

    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        for re in res:
            re['secondary_uom_id'] = self.secondary_uom_id.id
            re['secondary_quantity'] = self.secondary_quantity
        return res
