from odoo import models, fields


class JobPosition(models.Model):
    _name = "onboarding_app.job.position"
    _description = "Job Position"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    description = fields.Text(required=True)
    department_id = fields.Many2one("onboarding_app.department", string="Department")
