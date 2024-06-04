from odoo import models, fields


class TaskType(models.Model):
    _name = "onboarding_app.task.type"
    _description = "Task Type"

    name = fields.Char(required=True)

    def __str__(self):
        return self.title
