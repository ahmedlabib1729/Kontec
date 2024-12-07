# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_backorder = fields.Boolean('Have Backorder?', compute='cal_backorders', store=True)
    total_backorders = fields.Integer('Total Backorders', compute='cal_backorders', store=True)

    @api.depends('picking_ids')
    def cal_backorders(self):
        sale_orders = self.filtered('picking_ids')
        if sale_orders:
            stock_pickings = self.env['stock.picking'].search([
                ('sale_id', 'in', sale_orders.ids), 
                ('backorder_id', '!=', False)
            ])
            for order in sale_orders:
                related_pickings = stock_pickings.filtered(lambda p: p.sale_id.id == order.id)
                order.is_backorder = bool(related_pickings)
                order.total_backorders = len(related_pickings)

    def view_backorders(self):
        list_view_id = self.env.ref('stock.vpicktree').id
        form_view_id = self.env.ref('stock.view_picking_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Backorders'),
            'res_model': 'stock.picking',
            'view_type': 'form',
            'view_mode': 'list,form',
            'views': [(list_view_id, 'list'), (form_view_id, 'form')],
            'domain': [('sale_id', '=', self.id), ('backorder_id', '!=', False)],
            'context': {'default_sale_id': self.id},
        }
