from odoo import models, fields


class Tag(models.Model):
    _name = "onboarding_app.tag"
    _description = "Tag"

    name = fields.Char(required=True)
