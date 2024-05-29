from odoo import fields, models


class OnboardingStage(models.Model):
    _name = "onboarding_app.onboarding.stage"
    _description = "Onboarding Stage"
    _order = "sequence"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(default=False)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("sent for approval", "Sent For Approval"),
            ("approved", "Approved"),
            ("ongoing", "Ongoing"),
            ("email invited", "Email Invited"),
            ("confirm", "Confirm"),
        ],
        default="draft",
    )
