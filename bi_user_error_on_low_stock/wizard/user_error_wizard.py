# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class UserErrorWizard(models.TransientModel):
     _name = "user.error.wizard"
     _description = "User Error Wizard"

     message = fields.Text('Message', readonly=True)
