from odoo import api, exceptions, fields, models


class EmailInvitedWizard(models.Model):
    _name = "onboarding_app.onboarding.email.invited.wizard"
    _description = "Email Invited Wizard"

    ongoing_id = fields.Many2one(
        "onboarding_app.onboarding",
        "Email Invited",
        readonly=True,
        required=True,
        ondelete="cascade",
    )

    @api.model
    def default_get(self, fields):
        res = super(EmailInvitedWizard, self).default_get(fields)
        active_id = self.env.context.get("active_id")
        active_model = self.env.context.get("active_model")
        if not active_model == "onboarding_app.onboarding" or not active_id:
            raise exceptions.UserError(
                "You can only use this wizard from onboarding form"
            )

        if not res.get("ongoing_id") and active_id:
            res["ongoing_id"] = active_id

        return res

    def action_confirm(self):
        if self.ongoing_id:
            email_invited = self.env.ref(
                "onboarding_app.onboarding_stage_email_invited"
            )
            # self.ongoing_id.onboarding_task_list_id.sudo().write(
            #     {"status": "completed"}
            # )

            self.ongoing_id.sudo().write({"stage_id": email_invited.id})

        print("Email Invited")
