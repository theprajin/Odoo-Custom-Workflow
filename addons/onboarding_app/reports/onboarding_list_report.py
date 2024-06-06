from odoo import api, models


class OnboardingListReport(models.Abstract):
    _name = "report.onboaring_list_report"

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = [("job_position_id", "in", docids)]
        onboarding = self.env["onboarding_app.onboarding"].search(domain)

        pass
