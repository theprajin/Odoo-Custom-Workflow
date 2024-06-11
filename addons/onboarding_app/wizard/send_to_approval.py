from odoo import api, exceptions, fields, models


class SendToApprovalWizard(models.TransientModel):
    _name = "onboarding_app.onboarding.sendtoapproval.wizard"
    _description = "Send to Approval"

    draft_id = fields.Many2one(
        "onboarding_app.onboarding",
        "Draft",
        required=True,
        ondelete="cascade",
    )

    @api.model
    def default_get(self, fields):
        res = super(SendToApprovalWizard, self).default_get(fields)
        active_id = self.env.context.get("active_id")
        active_model = self.env.context.get("active_model")
        if not active_model == "onboarding_app.onboarding" or not active_id:
            raise exceptions.UserError(
                "You can only use this wizard from onboarding form"
            )

        if not res.get("draft_id") and active_id:
            res["draft_id"] = active_id

        return res

    def action_confirm(self):
        print(self.draft_id)
        if self.draft_id:
            print("we are here")
            sent_to_approval = self.env.ref(
                "onboarding_app.onboarding_stage_sent_for_approval"
            )
            self.draft_id.sudo().write({"stage_id": sent_to_approval.id})
            # print("Message: Sent to approval")
        print("this is the message")
        return True
