# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    _description = 'Register Payment'
    
    analytic_distribution = fields.Json()
    analytic_precision = fields.Integer(store=False,
        default=lambda self: self.env['decimal.precision'].precision_get("Percentage Analytic"),)

    def action_create_payments(self):
        payments = self._create_payments()
        active_ids = self._context.get('active_id')
        move_ids = self.env['account.move'].browse(active_ids)

        for rec in self:
            if move_ids:
                for move in move_ids:
                    if move.line_ids:
                        for line in move.line_ids:
                            if line.analytic_distribution : 
                               line.analytic_distribution = rec.analytic_distribution
                            else:
                                if line.account_type == 'income':
                                   line.analytic_distribution = rec.analytic_distribution
            if payments:
                for payment in payments:
                    payment.analytic_distribution = rec.analytic_distribution
                    if payment.move_id:
                        for line in payment.move_id.line_ids:
                            if line.account_type == 'asset_current':
                                line.analytic_distribution = rec.analytic_distribution

        if self._context.get('dont_redirect_to_payments'):
            return True

        action = {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'context': {'create': False},
        }
        if len(payments) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': payments.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', payments.ids)],
            })
        return action

