from odoo import models, fields


class TaskType(models.Model):
    _name = "onboarding_app.task.type"
    _description = "Task Type"

    title = fields.Char(required=True)
