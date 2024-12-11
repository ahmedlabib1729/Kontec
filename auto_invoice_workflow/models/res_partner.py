from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    workflow_id = fields.Many2one(
        'sh.auto.sale.workflow', string="Sale Workflow")
