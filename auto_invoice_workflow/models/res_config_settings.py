from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    group_auto_sale_workflow = fields.Boolean("Enable Auto Workflow")
    workflow_id = fields.Many2one(
        'sh.auto.sale.workflow', string="Default Workflow")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_auto_sale_workflow = fields.Boolean("Enable Auto Workflow", related="company_id.group_auto_sale_workflow",
                                              readonly=False, implied_group='auto_invoice_workflow.group_auto_sale_workflow')
    workflow_id = fields.Many2one(
        'sh.auto.sale.workflow', string="Default Workflow", related="company_id.workflow_id", readonly=False)
