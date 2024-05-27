from odoo import models, fields


class Task(models.Model):
    _name = "onboarding_app.task"
    _description = "Task"

    title = fields.Char(required=True)
    description = fields.Char(size=25)
    # type_id = fields.Many2one()
    # job_position_id = fields.Many2one()
    deadline = fields.Integer()
