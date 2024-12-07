# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError
from collections import defaultdict

class StockMove(models.Model):
	_inherit = 'stock.move'

	secondary_uom_id = fields.Many2one('uom.uom', compute='_quantity_secondary_compute', string="Secondary UOM", store=True)
	secondary_quantity = fields.Float('Secondary Qty', compute='_quantity_secondary_compute', digits='Product Unit of Measure', store=True)
	secondary_done_qty = fields.Float('Secondary Quantity Done', compute='_quantity_secondary_done_compute', digits='Product Unit of Measure', inverse='_quantity_secondary_done_set')
 
	@api.depends('product_id', 'product_uom_qty','secondary_uom_id')
	def _quantity_secondary_compute(self):
		for order in self:
			if order.product_id.secondary_uom:
				order.secondary_uom_id = order.product_id.secondary_uom_id
				uom_quantity = order.product_id.uom_id._compute_quantity(order.product_uom_qty, order.secondary_uom_id, rounding_method='HALF-UP')
				order.secondary_quantity = uom_quantity

	@api.depends('quantity', 'move_line_ids.quantity', 'move_line_ids.secondary_done_qty', 'move_line_ids.secondary_uom_id')
	def _quantity_secondary_done_compute(self):
		if not any(self._ids):
			# onchange
			for move in self:
				quantity = 0
				if move.move_line_ids:
					for move_line in move.move_line_ids:
						if move_line.product_uom_id.category_id and move.secondary_uom_id.category_id:
							if move_line.product_uom_id.category_id == move.secondary_uom_id.category_id:
								quantity += move_line.product_uom_id._compute_quantity(
									move_line.quantity, move.secondary_uom_id, round=False)
					move.secondary_done_qty = quantity
		else:
			# compute
			move_lines = self.env['stock.move.line']
			for move in self:
				move_lines |= move.move_line_ids

			data = self.env['stock.move.line'].read_group(
				[('id', 'in', move_lines.ids)],
				['move_id', 'product_uom_id', 'quantity'], ['move_id', 'product_uom_id'],
				lazy=False
			)

			rec = defaultdict(list)
			for d in data:
				rec[d['move_id'][0]] += [(d['product_uom_id'][0], d['quantity'])]

			for move in self:
				uom = move.secondary_uom_id
				if uom:
					if move.product_id.uom_id.category_id == uom.category_id:
						move.secondary_done_qty = sum(
							self.env['uom.uom'].browse(line_uom_id)._compute_quantity(qty, uom, round=False)
							for line_uom_id, qty in rec.get(move.ids[0] if move.ids else move.id, [])
						)
				else:
					move.secondary_done_qty = 0.0

 
	def _quantity_secondary_done_set(self):
		quantity = self[0].secondary_done_qty  # any call to create will invalidate `move.quantity`
		for move in self:
			move_lines = move.move_line_ids
			if not move_lines:
				if quantity:
					# do not impact reservation here
					move_line = self.env['stock.move.line'].create(dict(move._prepare_move_line_vals(), quantity=quantity))
					move.write({'move_line_ids': [(4, move_line.id)]})
			elif len(move_lines) == 1:
				move_lines[0].secondary_done_qty = quantity
			else:
				# Bypass the error if we're trying to write the same value.
				ml_quantity_done = 0
				for move_line in move_lines:
					ml_quantity_done += move_line.product_uom_id._compute_quantity(move_line.quantity, move.secondary_uom_id, round=False)
				if float_compare(quantity, ml_quantity_done, precision_rounding=move.secondary_uom_id.rounding) != 0:
					raise UserError(_("Cannot set the done quantity from this stock move, work directly with the move lines."))

	def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
		res = super(StockMove, self)._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
		if res:
			res.update({
				'secondary_uom_id': self.secondary_uom_id and self.secondary_uom_id.id or False,
			})
			if quantity:
				if self.product_id.secondary_uom:
					uom_quantity = self.product_id.uom_id._compute_quantity(quantity, self.secondary_uom_id, rounding_method='HALF-UP')
					uom_quantity_back_to_product_uom = self.secondary_uom_id._compute_quantity(uom_quantity, self.product_id.uom_id, rounding_method='HALF-UP')
					rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
					if float_compare(quantity, uom_quantity_back_to_product_uom, precision_digits=rounding) == 0:
						res = dict(res, secondary_quantity=uom_quantity)
					else:
						res = dict(res, secondary_quantity=uom_quantity, product_uom_id=self.product_id.uom_id.id)
		return res


class StockMoveLine(models.Model):
	_inherit = 'stock.move.line'

	secondary_uom_id = fields.Many2one('uom.uom', string="Secondary UOM",compute="_compute_secondary_qty" ,store=True)
	secondary_quantity = fields.Float("Secondary Qty", digits='Product Unit of Measure' ,compute="_compute_secondary_qty" ,store=True)
	secondary_done_qty = fields.Float("Secondary Done Qty", digits='Product Unit of Measure')


	@api.depends('product_id','product_id.uom_id','quantity','quantity','product_id.secondary_uom_id')
	def _compute_secondary_qty(self):
		for move_line in self:
			if move_line.product_id.secondary_uom:
				move_line.update({'secondary_uom_id' : move_line.product_id.secondary_uom_id})
				uom_quantity = move_line.product_id.uom_id._compute_quantity(move_line.quantity or move_line.quantity, move_line.product_id.secondary_uom_id, rounding_method='HALF-UP')
				move_line.update({'secondary_quantity' : uom_quantity})
				uom_done_quantity = move_line.product_id.uom_id._compute_quantity(move_line.quantity, move_line.product_id.secondary_uom_id, rounding_method='HALF-UP')
				move_line.update({'secondary_done_qty' : uom_done_quantity})


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4::