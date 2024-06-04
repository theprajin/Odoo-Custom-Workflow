from odoo import models, fields


class Department(models.Model):
    _name = "onboarding_app.department"
    _description = "department description"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
