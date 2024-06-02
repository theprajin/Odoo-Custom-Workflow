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

    onboarding_id = fields.Many2one("onboarding_app.onboarding")
    title = fields.Char(required=True)
    description = fields.Char(required=True)
    description = fields.Char(string="Description")
    deadline = fields.Integer(string="Deadline(days)", required=True)

    # @api.depends("task_id")
    # def _compute_title(self):
    #     for record in self:
    #         task_titles = ", ".join(record.task_id.mapped("title"))
    #         record.title = task_titles or "No Tasks"

    # def tasks(self):
    #     task_list = []
    #     task_related_to_job_positon = self.env["onboarding_app.task"].search(
    #         [("job_position_id", "=", "onboarding_id.job_position_id")]
    #     )
    #     for task in task_related_to_job_positon:
    #         data = {
    #             "title": task.title,
    #             "description": task.description,
    #         }
    #         task_list.append((0, 0, data))
    #         return task_list


class Onboarding(models.Model):
    _name = "onboarding_app.onboarding"
    _description = "Onboarding"
    _inherit = ["mail.thread", "mail.activity.mixin"]

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
        compute="_compute_onboarding_task_list",
        store=True,
        readonly=False,
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
    state = fields.Selection(related="stage_id.state", tracking=True)

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search(domain, order=order)

    @api.depends()
    def _compute_onboarding_task_list(self):
        print("here we are")
        tasks = self.env["onboarding_app.task"].search([])
        task_list = [
            (
                0,
                0,
                {
                    "title": task.title,
                    "description": task.description,
                    "deadline": task.deadline,
                },
            )
            for task in tasks
        ]
        self.onboarding_task_list_id = task_list
