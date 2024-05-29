from odoo import api, exceptions, fields, models


class SendToApprovalWizard(models.TransientModel):
    _name = "onboarding_app.onboarding.sendtoapproval.wizard"
    _description = "Send to Approval"

    def button_confirm(self):
        print("Sent to approval")
