from odoo import fields, models


class ResUser(models.Model):
    _inherit = "res.users"

    # email = fields.Char(
    #     related="partner_id.email", string="Email", store=True, readonly=False
    # )
    # phone = fields.Char(
    #     related="partner_id.phone", string="Phone", store=True, readonly=False
    # )
