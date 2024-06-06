from datetime import timedelta, date
import re
import random
import string
from odoo import models, fields, api, exceptions


class OnboardingLine(models.Model):
    _name = "onboarding_app.onboarding.line"
    _description = "Onboarding Line"

    onboarding_id = fields.Many2one(
        "onboarding_app.onboarding",
        required=True,
        ondelete="cascade",
    )

    remark = fields.Char("Remark")


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
        "onboarding_app.onboarding",
        required=True,
        ondelete="cascade",
    )

    document = fields.Binary(string="Document", store=True, required=True)
    name = fields.Char("Name", required=True)
    document_number = fields.Char("Document Number")
    document_filename = fields.Char("Document Filename", store=True)
    description = fields.Char("Description")


class ExtraInformationLine(models.Model):
    _name = "onboarding_app.extra.information.line"
    _description = "Extra Information Line"

    extra_information_line_id = fields.Many2one(
        "onboarding_app.onboarding", required=True, ondelete="cascade"
    )
    extra_information = fields.Char("Extra Information")


class OnboardingTaskListRemarkLine(models.Model):
    _name = "onboarding_app.onboarding.task.remark"
    _description = "Onboarding Task List Remark"

    onboarding_task_list_id = fields.Many2one(
        "onboarding_app.onboarding.task.list", required=True, ondelete="cascade"
    )
    remark = fields.Char("Approval Remark")


class OnboardingTaskListDocumentLine(models.Model):
    _name = "onboarding_app.onboarding.task.document"
    _description = "Onboarding Task List Document"

    onboarding_task_list_id = fields.Many2one(
        "onboarding_app.onboarding.task.list", required=True, ondelete="cascade"
    )
    document = fields.Binary(string="Document")
    name = fields.Char("Name", required=True)
    document_number = fields.Char("Document Number")
    document_filename = fields.Char("Document Filename", store=True)
    description = fields.Char("Description")


class OnboardingTaskList(models.Model):
    _name = "onboarding_app.onboarding.task.list"
    _description = "Onboarding Task List"

    onboarding_id = fields.Many2one("onboarding_app.onboarding", ondelete="cascade")
    title = fields.Char(required=True)
    description = fields.Char(required=True)
    deadline = fields.Date(string="Deadline(days)", default=fields.Date.today)
    assign_to = fields.Many2one("res.users", ondelete="cascade")
    is_task_complete = fields.Boolean(string="Is Task Complete", default=False)
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("assigned", "Assigned"),
            ("completed", "Completed"),
        ],
        default="draft",
    )

    remark_line_id = fields.One2many(
        "onboarding_app.onboarding.task.remark",
        "onboarding_task_list_id",
        string="Remarks",
    )

    document_line_id = fields.One2many(
        "onboarding_app.onboarding.task.document",
        "onboarding_task_list_id",
        string="Document",
    )

    @api.onchange("assign_to")
    def _compute_task_status(self):
        for task in self:
            if task.assign_to and task.status != "completed":
                task.status = "assigned"
            elif not task.assign_to:
                task.status = "draft"

    @api.depends()
    def _compute_deadline_date(self):
        pass

    def btn_complete(self):
        for record in self:
            record.status = "completed"
            record.is_task_complete = True
        return {
            "type": "ir.actions.act_window_close",
        }


class Onboarding(models.Model):
    _name = "onboarding_app.onboarding"
    _description = "Onboarding"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    title = fields.Char(required=True, tracking=True)
    name = fields.Char(required=True, tracking=True)
    email = fields.Char(required=True, tracking=True)
    password1 = fields.Char()
    phone = fields.Char(size=14, required=True, tracking=True)
    # Address Fields
    street = fields.Char("Street", readonly=False)
    street2 = fields.Char("Street", readonly=False)
    zip = fields.Char("Zip", readonly=False)
    city = fields.Char("City", readonly=False)
    state_id = fields.Many2one(
        "res.country.state",
        string="State",
        readonly=False,
        domain="[('country_id', '=?', country_id)] ",
    )
    country_id = fields.Many2one("res.country", string="Country", readonly=False)

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
    completed_task_count = fields.Integer(
        string="Task Completion %",
        compute="_compute_completed_task_count",
        store=True,
    )

    is_email_sent = fields.Boolean(default=False)

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

    stage_id = fields.Many2one(
        "onboarding_app.onboarding.stage",
        string="Stage",
        default=lambda s: s._default_onboarding_stage_id(),
        group_expand="_group_expand_stage_id",
    )
    state = fields.Selection(related="stage_id.state", tracking=True)

    _sql_constraints = [
        (
            "name_uniq",
            "UNIQUE (email, phone)",
            "Onboarding with this email and phone already exists",
        ),
    ]

    @api.model
    def _default_onboarding_stage_id(self):
        Stage = self.env["onboarding_app.onboarding.stage"]
        return Stage.search([("state", "=", "draft")], limit=1)

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search(domain, order=order)

    @api.onchange("email")
    def _check_email(self):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        for record in self:
            if record.email and not re.fullmatch(regex, record.email):
                warning = {
                    "title": "Invalid Email",
                    "message": "The email address you entered is not valid",
                }
                # raise exceptions.ValidationError("Invalid Email")
                return {"warning": warning}

    @api.onchange("phone")
    def _check_phone(self):
        regex = "^\\+?[1-9][0-9]{7,14}$"
        for record in self:
            if record.phone and not re.match(regex, record.phone):
                warning = {
                    "title": "Invalid Phone",
                    "message": "The phone number you entered is invalid",
                }
                # raise exceptions.ValidationError("Invalid Phone Number")
                return {"warning": warning}

    @api.onchange("department_id")
    def _onchange_department_id(self):
        self.job_position_id = False
        return {
            "domain": {
                "job_position_id": [("department_id", "=", self.department_id.id)]
            }
        }

    @api.depends("onboarding_task_list_id.status")
    def _compute_completed_task_count(self):
        for record in self:
            total_tasks = len(record.onboarding_task_list_id)
            completed_tasks = record.onboarding_task_list_id.filtered(
                lambda task: task.status == "completed"
            )
            if total_tasks > 0:
                completion_percentage = (len(completed_tasks) / total_tasks) * 100
                record.completed_task_count = int(completion_percentage)
                # print(completion_percentage)
            else:
                record.completed_task_count = 0

    def populate_onboarding_task_list(self):
        # call this for onchange in job position id
        for onboarding in self:
            job_position_id = onboarding.job_position_id.id
            if job_position_id:
                tasks = self.env["onboarding_app.task"].search(
                    [("job_position_id", "=", job_position_id)]
                )
                self.onboarding_task_list_id = [(5, 0, 0)]
                task_list = []
                for task in tasks:
                    deadline_date = date.today() + timedelta(task.deadline)
                    task_list.append(
                        (
                            0,
                            0,
                            {
                                "title": task.name,
                                "description": task.description,
                                "status": "draft",
                                "deadline": deadline_date,
                            },
                        )
                    )

                self.onboarding_task_list_id = task_list

    # genenrate random text of 6 characters for password
    # @api.depends()
    def generate_random_text(self, length=6):
        # letters = string.ascii_letters + string.digits
        # for record in self:
        #     record.password = "".join(random.choice(letters) for i in range(length))
        letters = string.ascii_letters + string.digits
        return "".join(random.choice(letters) for i in range(length))

    # set user password
    def set_user_password(self):
        self.ensure_one()

        # self.user_id.sudo().write({"password": self.generate_random_text()})
        self.password1 = self.generate_random_text()
        # self.user_id.new_password = self.password1
        # self.user_id._cr.commit()
        self.user_id.sudo().write({"new_password": self.password1})

    # btn for email invitation
    def action_email_invite(self):
        email_invited = self.env.ref("onboarding_app.onboarding_stage_email_invited")

        ctx = {
            "default_model": "onboarding_app.onboarding",
            "default_res_id": self.id,
            "default_use_template": True,
            "default_template_id": self.env.ref(
                "onboarding_app.send_email_invitation_template"
            ).id,
            "default_composition_mode": "comment",
            "mark_onboard_as_sent": True,  # use this context
            "default_email_layout_xmlid": "mail.mail_notification_layout_with_responsible_signature",
            "force_email": True,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }


# email, pdf
