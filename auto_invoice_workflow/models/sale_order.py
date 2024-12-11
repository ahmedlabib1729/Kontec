from odoo import api, Command, fields, models, _
from odoo.tools import format_amount, format_date, formatLang, groupby
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import UserError, ValidationError


MAP_INVOICE_TYPE_PARTNER_TYPE = {
    'out_invoice': 'customer',
    'out_refund': 'customer',
    'out_receipt': 'customer',
    'in_invoice': 'supplier',
    'in_refund': 'supplier',
    'in_receipt': 'supplier',
}


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    workflow_id = fields.Many2one(
        'sh.auto.sale.workflow', string="Sale Workflow",compute='calc_workflow_id')
    is_boolean = fields.Boolean(related="company_id.group_auto_sale_workflow")

    def calc_workflow_id(self):
        for r in self:
            workflow = self.env['sh.auto.sale.workflow'].sudo().search([('type','=','sale')],limit=1)
            r.workflow_id = workflow.id if workflow else False


    # @api.onchange('partner_id')
    # def get_workflow(self):
    #     if self.partner_id.workflow_id:
    #         if self.company_id.group_auto_sale_workflow:
    #             self.workflow_id = self.partner_id.workflow_id
    #     else:
    #         if self.company_id.group_auto_sale_workflow and self.company_id.workflow_id:
    #             self.workflow_id = self.company_id.workflow_id

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.workflow_id:
            if self.workflow_id.validate_order and self.picking_ids:
                if self.workflow_id.force_transfer:
                    for picking in self.picking_ids:
                        for stock_move in picking.move_ids_without_package:
                            if stock_move.move_line_ids:
                                stock_move.move_line_ids.update({
                                    'quantity': stock_move.product_uom_qty,
                                })
                            else:
                                self.env['stock.move.line'].create({
                                    'picking_id': picking.id,
                                    'move_id': stock_move.id,
                                    'date': stock_move.date,
                                    'reference': stock_move.reference,
                                    'origin': stock_move.origin,
                                    'quantity': stock_move.product_uom_qty,
                                    'product_id': stock_move.product_id.id,
                                    'product_uom_id': stock_move.product_uom.id,
                                    'location_id': stock_move.location_id.id,
                                    'location_dest_id': stock_move.location_dest_id.id
                                })
                        picking.with_context().button_validate()
                        if picking.state != 'done':
                            sms = self.env['confirm.stock.sms'].create({
                                'pick_ids': [(4, picking.id)],
                            })
                            sms.send_sms()
                            picking.button_validate()

                else:
                    for picking in self.picking_ids:
                        picking.button_validate()
                        # wiz = self.env['stock.immediate.transfer'].create({
                        #     'pick_ids': [(4, picking.id)],
                        #     'immediate_transfer_line_ids': [(0, 0, {
                        #         'picking_id': picking.id,
                        #         'to_immediate': True,
                        #     })]
                        # })
                        # wiz.with_context(
                        #     button_validate_picking_ids=picking.ids).process()

                        if picking.state != 'done':
                            sms = self.env['confirm.stock.sms'].create({
                                'pick_ids': [(4, picking.id)],
                            })
                            sms.send_sms()
                            ret = picking.button_validate()
                            # if 'res_model' in ret and ret['res_model'] == 'stock.backorder.confirmation':
                            #     backorder_wizard = self.env['stock.backorder.confirmation'].create({
                            #         'pick_ids': [(4, picking.id)],
                            #         'backorder_confirmation_line_ids': [(0, 0, {
                            #             'picking_id': picking.id,
                            #             'to_backorder': True,
                            #
                            #         })]
                            #     })
                            #     backorder_wizard.with_context(
                            #         button_validate_picking_ids=picking.ids).process()

            if self.workflow_id.create_invoice:
                invoice = self._create_invoices()
                if self.workflow_id.sale_journal:
                    invoice.write({
                        'journal_id': self.workflow_id.sale_journal.id
                    })

                if self.workflow_id.validate_invoice:
                    invoice.action_post()

                    if self.workflow_id.send_invoice_by_email:
                        template_id = self.env.ref(
                            'account.email_template_edi_invoice')
                        if template_id:
                            template_id.auto_delete = False
                            invoice.sudo()._generate_pdf_and_send_invoice(template_id)

                    if self.workflow_id.register_payment:

                        # payment_methods = self.env['account.payment.method'].search([('payment_type','=','inbound')])
                        # journal = self.env['account.journal'].search([('type','in',('bank','cash'))])
                        payment = self.env['account.payment'].create({
                            'currency_id': invoice.currency_id.id,
                            'amount': invoice.amount_total,
                            'payment_type': 'inbound',
                            'partner_id': invoice.commercial_partner_id.id,
                            'partner_type': MAP_INVOICE_TYPE_PARTNER_TYPE[invoice.move_type],
                            'payment_reference': invoice.payment_reference or invoice.name,
                            'payment_method_id': self.workflow_id.payment_method.id,
                            'journal_id': self.workflow_id.payment_journal.id
                        })

                        payment.action_post()
                        payment.invoice_ids = invoice.ids
                        # line_id = payment.line_ids.filtered(lambda l: l.credit)
                        # invoice.js_assign_outstanding_line(line_id.id)
        return res
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    workflow_id = fields.Many2one(
        'sh.auto.sale.workflow', string="Sale Workflow", compute='calc_workflow_id')
    is_boolean = fields.Boolean(related="company_id.group_auto_sale_workflow")

    def calc_workflow_id(self):
        for r in self:
            workflow = self.env['sh.auto.sale.workflow'].sudo().search([('type', '=', 'purchase')], limit=1)
            r.workflow_id = workflow.id if workflow else False

    # @api.onchange('partner_id')
    # def get_workflow(self):
    #     if self.partner_id.workflow_id:
    #         if self.company_id.group_auto_sale_workflow:
    #             self.workflow_id = self.partner_id.workflow_id
    #     else:
    #         if self.company_id.group_auto_sale_workflow and self.company_id.workflow_id:
    #             self.workflow_id = self.company_id.workflow_id
    def create_bill(self):
        """Create the invoice associated to the PO.
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        # 1) Prepare invoice vals and clean-up the section lines
        invoice_vals_list = []
        sequence = 10
        for order in self:
            if order.invoice_status != 'to invoice':
                continue

            order = order.with_company(order.company_id)
            pending_section = None
            # Invoice values.
            invoice_vals = order._prepare_invoice()
            # Invoice line values (keep only necessary sections).
            for line in order.order_line:
                if line.display_type == 'line_section':
                    pending_section = line
                    continue
                if not float_is_zero(line.qty_to_invoice, precision_digits=precision):
                    if pending_section:
                        line_vals = pending_section._prepare_account_move_line()
                        line_vals.update({'sequence': sequence})
                        invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
                        sequence += 1
                        pending_section = None
                    line_vals = line._prepare_account_move_line()
                    line_vals.update({'sequence': sequence})
                    invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
                    sequence += 1
            invoice_vals_list.append(invoice_vals)

        if not invoice_vals_list:
            raise UserError(_('There is no invoiceable line. If a product has a control policy based on received quantity, please make sure that a quantity has been received.'))

        # 2) group by (company_id, partner_id, currency_id) for batch creation
        new_invoice_vals_list = []
        for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: (x.get('company_id'), x.get('partner_id'), x.get('currency_id'))):
            origins = set()
            payment_refs = set()
            refs = set()
            ref_invoice_vals = None
            for invoice_vals in invoices:
                if not ref_invoice_vals:
                    ref_invoice_vals = invoice_vals
                else:
                    ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                origins.add(invoice_vals['invoice_origin'])
                payment_refs.add(invoice_vals['payment_reference'])
                refs.add(invoice_vals['ref'])
            ref_invoice_vals.update({
                'ref': ', '.join(refs)[:2000],
                'invoice_origin': ', '.join(origins),
                'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
            })
            new_invoice_vals_list.append(ref_invoice_vals)
        invoice_vals_list = new_invoice_vals_list

        # 3) Create invoices.
        moves = self.env['account.move']
        AccountMove = self.env['account.move'].with_context(default_move_type='in_invoice')
        for vals in invoice_vals_list:
            moves |= AccountMove.with_company(vals['company_id']).create(vals)

        # 4) Some moves might actually be refunds: convert them if the total amount is negative
        # We do this after the moves have been created since we need taxes, etc. to know if the total
        # is actually negative or not
        moves.filtered(lambda m: m.currency_id.round(m.amount_total) < 0).action_switch_move_type()
        return moves



    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        if self.workflow_id:
            if self.workflow_id.validate_order and self.picking_ids:
                if self.workflow_id.force_transfer:
                    for picking in self.picking_ids:
                        for stock_move in picking.move_ids_without_package:
                            if stock_move.move_line_ids:
                                stock_move.move_line_ids.update({
                                    'quantity': stock_move.product_uom_qty,
                                })
                            else:
                                self.env['stock.move.line'].create({
                                    'picking_id': picking.id,
                                    'move_id': stock_move.id,
                                    'date': stock_move.date,
                                    'reference': stock_move.reference,
                                    'origin': stock_move.origin,
                                    'quantity': stock_move.product_uom_qty,
                                    'product_id': stock_move.product_id.id,
                                    'product_uom_id': stock_move.product_uom.id,
                                    'location_id': stock_move.location_id.id,
                                    'location_dest_id': stock_move.location_dest_id.id
                                })
                        picking.with_context().button_validate()
                        if picking.state != 'done':
                            sms = self.env['confirm.stock.sms'].create({
                                'pick_ids': [(4, picking.id)],
                            })
                            sms.send_sms()
                            picking.button_validate()

                else:
                    for picking in self.picking_ids:
                        picking.button_validate()
                        # wiz = self.env['stock.immediate.transfer'].create({
                        #     'pick_ids': [(4, picking.id)],
                        #     'immediate_transfer_line_ids': [(0, 0, {
                        #         'picking_id': picking.id,
                        #         'to_immediate': True,
                        #     })]
                        # })
                        # wiz.with_context(
                        #     button_validate_picking_ids=picking.ids).process()

                        if picking.state != 'done':
                            sms = self.env['confirm.stock.sms'].create({
                                'pick_ids': [(4, picking.id)],
                            })
                            sms.send_sms()
                            ret = picking.button_validate()
                            # if 'res_model' in ret and ret['res_model'] == 'stock.backorder.confirmation':
                            #     backorder_wizard = self.env['stock.backorder.confirmation'].create({
                            #         'pick_ids': [(4, picking.id)],
                            #         'backorder_confirmation_line_ids': [(0, 0, {
                            #             'picking_id': picking.id,
                            #             'to_backorder': True,
                            #
                            #         })]
                            #     })
                            #     backorder_wizard.with_context(
                            #         button_validate_picking_ids=picking.ids).process()

            if self.workflow_id.create_invoice:
                invoice = self.create_bill()
                if self.workflow_id.sale_journal:
                    invoice.write({
                        'journal_id': self.workflow_id.sale_journal.id,
                        'invoice_date': fields.Date.today()
                    })

                if self.workflow_id.validate_invoice:
                    invoice.action_post()

                    if self.workflow_id.send_invoice_by_email:
                        template_id = self.env.ref(
                            'account.email_template_edi_invoice')
                        if template_id:
                            template_id.auto_delete = False
                            invoice.sudo()._generate_pdf_and_send_invoice(template_id)

                    if self.workflow_id.register_payment:

                        # payment_methods = self.env['account.payment.method'].search([('payment_type','=','inbound')])
                        # journal = self.env['account.journal'].search([('type','in',('bank','cash'))])
                        payment = self.env['account.payment'].create({
                            'currency_id': invoice.currency_id.id,
                            'amount': invoice.amount_total,
                            'payment_type': 'outbound',
                            'partner_id': invoice.commercial_partner_id.id,
                            'partner_type': MAP_INVOICE_TYPE_PARTNER_TYPE[invoice.move_type],
                            'payment_reference': invoice.payment_reference or invoice.name,
                            'payment_method_id': self.workflow_id.payment_method.id,
                            'journal_id': self.workflow_id.payment_journal.id
                        })

                        payment.action_post()
                        payment.invoice_ids = invoice.ids
        return res