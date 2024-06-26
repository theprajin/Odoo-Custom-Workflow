from odoo import api, exceptions, fields, models


class OngoingWizard(models.TransientModel):
    _name = "onboarding_app.onboarding.ongoing.wizard"
    _description = "Ongoing wizard"

    approval_id = fields.Many2one(
        "onboarding_app.onboarding",
        "Ongoing",
        required=True,
        ondelete="cascade",
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
            print(self.approval_id.user_id)
            print(self.approval_id.user_id.password)
            print(self.approval_id.user_id.new_password)
            self.approval_id.sudo().write({"stage_id": ongoing.id})
            self.approval_id.populate_onboarding_task_list()

        # print("Ongoing")
