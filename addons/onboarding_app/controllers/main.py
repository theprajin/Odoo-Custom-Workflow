from odoo import http


class Main(http.Controller):
    @http.route("/onboarding", type="http", auth="public", website=True)
    def onboarding(self):
        Onboarding = http.request.env["onboarding_app.onboarding"]
        onboardings = Onboarding.sudo().search([])
        res = http.request.render(
            "onboarding_app.home",
            {"onboardings": onboardings},
        )

        return res
