# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.tools.float_utils import float_round

class AccountPayment(models.Model):
	_inherit = 'account.payment'

	analytic_distribution = fields.Json()
	analytic_precision = fields.Integer(store=False,
		default=lambda self: self.env['decimal.precision'].precision_get("Percentage Analytic"),)

	def action_post(self):
		res = super(AccountPayment, self).action_post()
		if not self.env.context.get('dont_redirect_to_payments'):
			for rec in self:
				if rec.analytic_distribution:
					if rec.move_id.line_ids:
						for line in rec.move_id.line_ids:
							if rec.amount == 0:
								if line.account_type == 'asset_current':
									line.analytic_distribution = rec.analytic_distribution
							else:
								if rec.payment_type == 'inbound':
									if line.account_type == 'asset_current' and line.debit > 0:
										line.analytic_distribution = rec.analytic_distribution
									if line.account_type == 'asset_receivable' and line.credit > 0:
										line.analytic_distribution = rec.analytic_distribution
								if rec.payment_type == 'outbound':
									if line.account_type == 'asset_current' and line.credit > 0:
										line.analytic_distribution = rec.analytic_distribution
									if line.account_type == 'asset_receivable' and line.debit > 0:
										line.analytic_distribution = rec.analytic_distribution

				if rec.paired_internal_transfer_payment_id:
					for pay in rec.paired_internal_transfer_payment_id.line_ids:
						if rec.paired_internal_transfer_payment_id.amount == 0:
							if pay.account_type == 'asset_current':
								pay.analytic_distribution = rec.analytic_distribution
						else:
							if rec.paired_internal_transfer_payment_id.payment_type == 'inbound':
								if pay.debit > 0:
								   pay.analytic_distribution = rec.analytic_distribution
								if pay.credit > 0:
								   pay.analytic_distribution = rec.analytic_distribution
							if rec.paired_internal_transfer_payment_id.payment_type == 'outbound':
								if pay.credit > 0:
								   pay.analytic_distribution = rec.analytic_distribution
								if pay.debit > 0:
								   pay.analytic_distribution = rec.analytic_distribution
		return res
