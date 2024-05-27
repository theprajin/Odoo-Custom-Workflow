from odoo import models, fields


class Onboarding(models.Model):
    _name = "onboarding_app.onboarding"
    _description = "Onboarding"

    name = fields.Char()
    description = fields.Text()
