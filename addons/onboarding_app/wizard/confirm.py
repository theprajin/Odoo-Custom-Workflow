from odoo import api, exceptions, fields, models


class ConfirmWizard(models.Model):
    _name = "onboarding_app.onboarding.confirm.wizard"
    _description = "Confirm wizard"

    email_invited_id = fields.Many2one(
        "onboarding_app.onboarding",
        "Confirm",
        readonly=True,
        required=True,
        ondelete="cascade",
    )

    @api.model
    def default_get(self, fields):
        res = super(ConfirmWizard, self).default_get(fields)
        active_id = self.env.context.get("active_id")
        active_model = self.env.context.get("active_model")
        if not active_model == "onboarding_app.onboarding" or not active_id:
            raise exceptions.UserError(
                "You can only use this wizard from onboarding form"
            )

        if not res.get("email_invited_id") and active_id:
            res["email_invited_id"] = active_id

        return res

    def action_confirm(self):
        if self.email_invited_id:
            confirm = self.env.ref("onboarding_app.onboarding_stage_confirm")
            self.email_invited_id.sudo().write({"stage_id": confirm.id})
        print("Confirm")
