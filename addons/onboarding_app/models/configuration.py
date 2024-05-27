from odoo import models, fields


class Configuration(models.Model):
    _name = "onboarding_app.configuration"
    _description = "Onboarding"

    name = fields.Char()
