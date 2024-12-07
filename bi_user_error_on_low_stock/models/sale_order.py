# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
class SaleOrder(models.Model):
	_inherit = "sale.order"

	def action_confirm(self):
		res = super(SaleOrder, self)
		for record in self:
			for rec in record.order_line:
				product_handon = rec.product_id.qty_available
				order_qty = rec.product_uom_qty
				if rec.product_id and product_handon and order_qty:
					if product_handon < order_qty:
						user_error_wizard_id = self.env['user.error.wizard'].create({
							'message': [f"Your available quantity of {i.product_id.name} is {i.product_id.qty_available}" for i in self.order_line if i.product_id.qty_available < i.product_uom_qty]
						})
						return {
								'name': _('User Error'),
								'type': 'ir.actions.act_window',
								'view_mode': 'form',
								'res_model': 'user.error.wizard',
								'res_id': user_error_wizard_id.id,
								'target': 'new',
						}
		return res.action_confirm()
