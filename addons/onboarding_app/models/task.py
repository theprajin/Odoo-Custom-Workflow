from odoo import models, fields


class Task(models.Model):
    _name = "onboarding_app.task"
    _description = "Task"

    title = fields.Char(required=True)
    description = fields.Char(size=25)
    type_id = fields.Many2one("onboarding_app.task.type", string="Type")
    job_position_id = fields.Many2one(
        "onboarding_app.job.position", string="Job Position"
    )
    deadline = fields.Integer(string="Deadline(days)")
    # assign_to = fields.Many2one("res.users", string="Assign To")
    # onboarding_task_list_id = fields.Many2many("onboarding_app.onboarding.task.list")
