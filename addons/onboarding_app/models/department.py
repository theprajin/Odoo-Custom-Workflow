from odoo import models, fields


class Department(models.Model):
    _name = "onboarding_app.department"
    _description = "department description"

    name = fields.Char()
