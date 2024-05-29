from odoo import models, fields


class OnboardingLine(models.Model):
    _name = "onboarding_app.onboarding.line"
    _description = "Onboarding Line"

    onboarding_id = fields.Many2one("onboarding_app.onboarding", required=True)
    remark = fields.Char("Remark")
    created_by = fields.Char("Created By")
    created_on = fields.Char("Created On")
    # approval_remark = fields.Char("Approval Remark")
    # document = fields.Char("Documents")
    # extra_information = fields.Char("Extra Information")


class ApprovalLine(models.Model):
    _name = "onboarding_app.approval.line"
    _description = "Approval Line"

    approval_line_id = fields.Many2one("onboarding_app.onboarding", required=True)
    approval_remark = fields.Char("Approval Remark")
    created_by = fields.Char("Created By")
    created_on = fields.Char("Created On")


class DocumentLine(models.Model):
    _name = "onboarding_app.document.document.line"
    _description = "Document Line"

    document_line_id = fields.Many2one("onboarding_app.onboarding", required=True)
    document = fields.Char("Documents")


class ExtraInformationLine(models.Model):
    _name = "onboarding_app.extra.information.line"
    _description = "Extra Information Line"

    extra_information_line_id = fields.Many2one(
        "onboarding_app.onboarding", required=True
    )
    extra_information = fields.Char("Extra Information")
