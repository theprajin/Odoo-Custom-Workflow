from odoo import models, fields, api, exceptions


class Task(models.Model):
    _name = "onboarding_app.task"
    _description = "Task"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    title = fields.Char(required=True)
    description = fields.Char(required=True)
    type_id = fields.Many2one("onboarding_app.task.type", string="Type")
    job_position_id = fields.Many2one(
        "onboarding_app.job.position", string="Job Position"
    )
    deadline = fields.Integer(string="Deadline(days)", required=True, tracking=True)

    _sql_constraints = [("title_uniq", "UNIQUE (title)", "Task title must be unique")]

    @api.constrains("deadline")
    def _check_deadline(self):
        for record in self:
            if record.deadline < 0:
                raise exceptions.ValidationError("Dealine Must Be A Positive Integer")
