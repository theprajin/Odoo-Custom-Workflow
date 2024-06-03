from odoo import api, exceptions, fields, models


class AppprovalWizard(models.Model):
    _name = "onboarding_app.onboarding.approval.wizard"
    _description = "Approval wizard"

    sent_to_approval_id = fields.Many2one(
        "onboarding_app.onboarding",
        "Sent to Approval",
        readonly=True,
        required=True,
        ondelete="cascade",
    )

    remark = fields.Char(required=True)

    approval_state = fields.Selection(
        [
            ("approve", "Approve"),
            ("reject", "Reject"),
        ],
        default="approve",
    )

    @api.model
    def default_get(self, fields):
        res = super(AppprovalWizard, self).default_get(fields)
        active_id = self.env.context.get("active_id")
        active_model = self.env.context.get("active_model")
        if not active_model == "onboarding_app.onboarding" or not active_id:
            raise exceptions.UserError(
                "You can only use this wizard from onboarding form"
            )

        if not res.get("sent_to_approval_id") and active_id:
            res["sent_to_approval_id"] = active_id

        return res

    def action_confirm(self):
        if self.approval_state == "approve":
            if self.sent_to_approval_id:
                approved = self.env.ref("onboarding_app.onboarding_stage_approved")
                self.sent_to_approval_id.sudo().write({"stage_id": approved.id})
                self.approval_remark_creation()
                self.approved_user_creation()
                
                # created_user = self.env["res.users"].search(
                #     [("name", "=", self.sent_to_approval_id.name)]
                # )
                # print(f"created User: {created_user}")
                # print("approve")

        elif self.approval_state == "reject":
            self.approval_remark_creation()

            print("reject")

    def approval_remark_creation(self):
        self.env["onboarding_app.approval.line"].create(
            {
                "approval_line_id": self.sent_to_approval_id.id,
                "approval_remark": self.remark,
            }
        )

    def approved_user_creation(self):
        onboarding = self.sent_to_approval_id
        self.env["res.users"].create(
            {
                "name": onboarding.name,
                "login": onboarding.email,
                "email": onboarding.email,
                "phone": onboarding.phone,
            }
        )
