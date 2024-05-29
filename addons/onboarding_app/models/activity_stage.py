from odoo import fields, models


class ActivityStage(models.Model):
    _name = "onboarding_app.onboarding.activity.stage"
    _description = "Activity Stage"
    _order = "sequence"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(default=False)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("assigned", "Assigned"),
            ("completed", "Completed"),
        ],
        default="draft",
    )
