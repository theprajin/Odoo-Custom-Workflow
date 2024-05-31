from odoo import api, exceptions, fields, models


class OngoingWizard(models.Model):
    _name = "onboarding_app.onboarding.ongoing.wizard"
    _description = "Ongoing wizard"

    approval_id = fields.Many2one(
        "onboarding_app.onboarding",
        "Ongoing",
        readonly=True,
        required=True,
    )

    @api.model
    def default_get(self, fields):
        res = super(OngoingWizard, self).default_get(fields)
        active_id = self.env.context.get("active_id")
        active_model = self.env.context.get("active_model")
        if not active_model == "onboarding_app.onboarding" or not active_id:
            raise exceptions.UserError(
                "You can only use this wizard from onboarding form"
            )

        if not res.get("approval_id") and active_id:
            res["approval_id"] = active_id

        return res

    def action_confirm(self):
        if self.approval_id:
            ongoing = self.env.ref("onboarding_app.onboarding_stage_ongoing")
            self.approval_id.sudo().write({"stage_id": ongoing.id})

        print("Ongoing")
