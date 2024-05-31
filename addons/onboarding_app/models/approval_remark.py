from odoo import api, models, fields


class ApprovalRemark(models.Model):
    _name = "onboarding_app.onboarding.approval.remark"
    _description = "Approval Remark"

    remark = fields.Char()
    approval_state = fields.Selection(
        [
            ("approve", "Approve"),
            ("reject", "Reject"),
        ],
    )
    create_by = fields.Many2one("res.user", "Created By")
