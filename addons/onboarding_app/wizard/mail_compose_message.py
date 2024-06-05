from odoo import api, exceptions, fields, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.model
    def context(self):

        return {
            "email_sent": True,
        }

    def _action_send_mail(self, auto_commit=False):
        res = super(MailComposeMessage, self)._action_send_mail(auto_commit=auto_commit)

        # Check if the model is 'onboarding_app.onboarding'
        if self.model == "onboarding_app.onboarding":
            onboarding_record = self.env[self.model].browse(self.res_id)

            if onboarding_record:
                if self.env.context.get("mark_onboard_as_sent"):
                    email_invited_stage = self.env.ref(
                        "onboarding_app.onboarding_stage_email_invited"
                    )
                    # Set the stage of the onboarding record to 'email invited'
                    onboarding_record.write({"stage_id": email_invited_stage.id})
                    onboarding_record.write({"is_email_sent": True})

        return res
