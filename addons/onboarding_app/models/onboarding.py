from odoo import models, fields, api


class OnboardingLine(models.Model):
    _name = "onboarding_app.onboarding.line"
    _description = "Onboarding Line"

    onboarding_id = fields.Many2one("onboarding_app.onboarding", required=True)
    remark = fields.Char("Remark")
    created_by = fields.Char("Created By")
    created_on = fields.Char("Created On")


class ApprovalLine(models.Model):
    _name = "onboarding_app.approval.line"
    _description = "Approval Line"

    approval_line_id = fields.Many2one("onboarding_app.onboarding", required=True)
    approval_remark = fields.Char("Approval Remark")


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


class OnboardingTaskList(models.Model):
    _name = "onboarding_app.onboarding.task.list"
    _description = "Onboarding Task List"

    onboarding_id = fields.Many2one("onboarding_app.onboarding", required=True)
    title = fields.Char()
    # description
    # task_id = fields.Many2many("onboarding_app.task")

    # @api.depends("task_id")
    # def _compute_title(self):
    #     for record in self:
    #         task_titles = ", ".join(record.task_id.mapped("title"))
    #         record.title = task_titles or "No Tasks"


class Onboarding(models.Model):
    _name = "onboarding_app.onboarding"
    _description = "Onboarding"

    title = fields.Char(required=True)
    name = fields.Char(required=True)
    email = fields.Char(required=True)
    phone = fields.Char(required=True)
    address = fields.Char(required=True)
    department_id = fields.Many2one(
        "onboarding_app.department", string="Department", required=True
    )
    job_position_id = fields.Many2one(
        "onboarding_app.job.position", string="Job Position", required=True
    )
    user_id = fields.Many2one("res.users", string="User")
    tags = fields.Many2many("onboarding_app.tag", string="Tags")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ]
    )
    is_nepali = fields.Boolean()
    experience = fields.Integer()
    website = fields.Char()
    age = fields.Integer()

    line_ids = fields.One2many(
        "onboarding_app.onboarding.line",
        "onboarding_id",
        string="Onboarding Features",
    )

    approval_line_id = fields.One2many(
        "onboarding_app.approval.line",
        "approval_line_id",
        string="Approval Features",
    )

    document_line_id = fields.One2many(
        "onboarding_app.document.document.line",
        "document_line_id",
        string="Document Uploading Feature",
    )

    extra_information_line_id = fields.One2many(
        "onboarding_app.extra.information.line",
        "extra_information_line_id",
        string="Extra Information",
    )

    onboarding_task_list_id = fields.One2many(
        "onboarding_app.onboarding.task.list",
        "onboarding_id",
        string="Onboarding Task List",
    )

    @api.model
    def _default_onboarding_stage_id(self):
        Stage = self.env["onboarding_app.onboarding.stage"]
        return Stage.search([("state", "=", "draft")], limit=1)

    stage_id = fields.Many2one(
        "onboarding_app.onboarding.stage",
        string="Stage",
        default=lambda s: s._default_onboarding_stage_id(),
        group_expand="_group_expand_stage_id",
    )
    state = fields.Selection(related="stage_id.state")

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search(domain, order=order)
