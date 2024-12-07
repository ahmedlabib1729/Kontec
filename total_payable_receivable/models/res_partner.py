# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Ammu Raj (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import api, fields, models
from odoo.tools import SQL


class ResPartner(models.Model):
    """Inheriting res_partner model"""
    _name = 'res.partner'
    _inherit = 'res.partner'

    partner_credit = fields.Monetary(compute='_compute_partner_credit',
                                     string='Total Receivable',
                                     help="Total amount this customer owes you."
                                     )
    partner_debit = fields.Monetary(compute='_compute_partner_credit',
                                    string='Total Payable',
                                    help="Total amount you have to pay to this "
                                         "vendor.")

    @api.depends_context('company')
    def _compute_partner_credit(self):
        """
          Retrieve the total receivable and payable amounts from customers
          for the current company.
        """
        query = self.env['account.move.line']._where_calc([
            ('parent_state', '=', 'posted'),
            ('company_id', 'child_of', self.env.company.root_id.id)
        ])
        self.env['account.move.line'].flush_model(
            ['account_id', 'amount_residual', 'company_id', 'parent_state',
             'partner_id', 'reconciled']
        )
        self.env['account.account'].flush_model(['account_type'])
        sql = SQL("""
                    SELECT account_move_line.partner_id, a.account_type, SUM(account_move_line.amount_residual)
                    FROM %s
                    LEFT JOIN account_account a ON (account_move_line.account_id=a.id)
                    WHERE a.account_type IN ('asset_receivable','liability_payable')
                    AND account_move_line.partner_id IN %s
                    AND account_move_line.reconciled IS NOT TRUE
                    AND %s
                    GROUP BY account_move_line.partner_id, a.account_type
                    """,
                  query.from_clause,
                  tuple(self.ids),
                  query.where_clause or SQL("TRUE"),
                  )
        treated = self.browse()
        for pid, account_type, val in self.env.execute_query(sql):
            partner = self.browse(pid)
            if account_type == 'asset_receivable':
                partner.partner_credit = val
                if partner not in treated:
                    partner.partner_debit = False
                    treated |= partner
            elif account_type == 'liability_payable':
                partner.partner_debit = -val
                if partner not in treated:
                    partner.partner_credit = False
                    treated |= partner
        remaining = (self - treated)
        remaining.partner_debit = False
        remaining.partner_credit = False
