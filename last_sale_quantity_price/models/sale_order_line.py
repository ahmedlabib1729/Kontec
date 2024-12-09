from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    free_qty = fields.Float(
         compute='_compute_quantities', search='_search_free_qty',
        compute_sudo=False, digits='Product Unit of Measure')

    def _search_free_qty(self, operator, value):
        domain = [('free_qty', operator, value)]
        product_variant_query = self.env['product.product']._search(domain)
        return [('product_variant_ids', 'in', product_variant_query)]



    @api.depends(
        'product_variant_ids.qty_available',
        'product_variant_ids.virtual_available',
        'product_variant_ids.incoming_qty',
        'product_variant_ids.outgoing_qty',
        'product_variant_ids.free_qty',
    )
    def _compute_quantities(self):
        res = self._compute_quantities_dict()
        for template in self:
            template.qty_available = res[template.id]['qty_available']
            template.virtual_available = res[template.id]['virtual_available']
            template.incoming_qty = res[template.id]['incoming_qty']
            template.outgoing_qty = res[template.id]['outgoing_qty']
            template.free_qty = res[template.id]['free_qty']

    def _compute_quantities_dict(self):
        variants_available = {
            p['id']: p for p in self.product_variant_ids._origin.read(['qty_available', 'virtual_available', 'incoming_qty', 'outgoing_qty','free_qty'])
        }
        prod_available = {}
        for template in self:
            qty_available = 0
            virtual_available = 0
            incoming_qty = 0
            outgoing_qty = 0
            free_qty = 0
            for p in template.product_variant_ids._origin:
                qty_available += variants_available[p.id]["qty_available"]
                virtual_available += variants_available[p.id]["virtual_available"]
                incoming_qty += variants_available[p.id]["incoming_qty"]
                outgoing_qty += variants_available[p.id]["outgoing_qty"]
                free_qty += variants_available[p.id]["free_qty"]
            prod_available[template.id] = {
                "qty_available": qty_available,
                "virtual_available": virtual_available,
                "incoming_qty": incoming_qty,
                "outgoing_qty": outgoing_qty,
                "free_qty": free_qty,
            }
        return prod_available


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    last_purchase_qty = fields.Float(string="Last Quantity", compute="_compute_last_purchase_qty_price")
    last_purchase_price = fields.Float(string="Last Price", compute="_compute_last_purchase_qty_price")

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
