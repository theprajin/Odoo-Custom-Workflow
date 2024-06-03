import re
from odoo import models, fields, api, exceptions


class OnboardingLine(models.Model):
    _name = "onboarding_app.onboarding.line"
    _description = "Onboarding Line"

    onboarding_id = fields.Many2one(
        "onboarding_app.onboarding", required=True, ondelete="cascade"
    )
    remark = fields.Char("Remark")
    created_by = fields.Char("Created By")
    created_on = fields.Char("Created On")


class ApprovalLine(models.Model):
    _name = "onboarding_app.approval.line"
    _description = "Approval Line"

    approval_line_id = fields.Many2one(
        "onboarding_app.onboarding", required=True, ondelete="cascade"
    )
    approval_remark = fields.Char("Approval Remark")


class DocumentLine(models.Model):
    _name = "onboarding_app.document.document.line"
    _description = "Document Line"

    document_line_id = fields.Many2one(
        "onboarding_app.onboarding", required=True, ondelete="cascade"
    )
    document = fields.Char("Documents")


class ExtraInformationLine(models.Model):
    _name = "onboarding_app.extra.information.line"
    _description = "Extra Information Line"

    extra_information_line_id = fields.Many2one(
        "onboarding_app.onboarding", required=True, ondelete="cascade"
    )
    extra_information = fields.Char("Extra Information")


class OnboardingTaskList(models.Model):
    _name = "onboarding_app.onboarding.task.list"
    _description = "Onboarding Task List"

    onboarding_id = fields.Many2one("onboarding_app.onboarding", ondelete="cascade")
    title = fields.Char(required=True)
    description = fields.Char(required=True)
    deadline = fields.Date(string="Deadline(days)", default=fields.Date.today)
    assign_to = fields.Many2one("res.users", ondelete="cascade")


class Onboarding(models.Model):
    _name = "onboarding_app.onboarding"
    _description = "Onboarding"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    title = fields.Char(required=True, tracking=True)
    name = fields.Char(required=True, tracking=True)
    email = fields.Char(required=True, tracking=True)
    phone = fields.Char(size=14, required=True, tracking=True)
    address = fields.Char(required=True)
    department_id = fields.Many2one(
        "onboarding_app.department", string="Department", required=True, tracking=True
    )
    job_position_id = fields.Many2one(
        "onboarding_app.job.position",
        string="Job Position",
        required=True,
        tracking=True,
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
        string="Remarks",
    )

    approval_line_id = fields.One2many(
        "onboarding_app.approval.line",
        "approval_line_id",
        string="Approval Remark",
    )

    document_line_id = fields.One2many(
        "onboarding_app.document.document.line",
        "document_line_id",
        string="Document",
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

    _sql_constraints = [
        (
            "name_uniq",
            "UNIQUE (email, phone)",
            "Onboarding with this email and phone already exists",
        ),
    ]

    @api.constrains("email")
    def _check_email(self):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        for record in self:
            if not re.fullmatch(regex, record.email):
                raise exceptions.ValidationError("Invalid Email")

    @api.constrains("phone")
    def _check_phone(self):
        regex = "^\\+?[1-9][0-9]{7,14}$"
        for record in self:
            if not re.match(regex, record.phone):
                raise exceptions.ValidationError("Invalid Phone Number")

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
    state = fields.Selection(related="stage_id.state", tracking=True)

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search(domain, order=order)

    def populate_onboarding_task_list(self):
        print("here we are")
        tasks = self.env["onboarding_app.task"].search([])
        task_list = [
            (
                0,
                0,
                {
                    "title": task.title,
                    "description": task.description,
                },
            )
            for task in tasks
        ]
        self.onboarding_task_list_id = task_list
