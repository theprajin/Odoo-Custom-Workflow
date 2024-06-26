from odoo import http


class Main(http.Controller):
    @http.route("/", type="http", auth="public", website=True)
    def onboarding(self):
        Onboarding = http.request.env["onboarding_app.onboarding"]
        onboardings = Onboarding.sudo().search([])
        res = http.request.render(
            "onboarding_app.home",
            {"onboardings": onboardings},
        )

        return res

    class UserController(http.Controller):

        @http.route("/users", type="http", auth="public", website=True)
        def users(self):
            user = http.request.env["res.users"]
            users = user.sudo().search([])
            res = http.request.render(
                "onboarding_app.users",
                {"users": users},
            )

            return res

    class OnboardingTaskListController(http.Controller):

        @http.route("/tasks", type="http", auth="public", website=True)
        def onboarding_list(self):
            onboarding_list = http.request.env["onboarding_app.onboarding.task.list"]
            task_list = onboarding_list.sudo().search([])
            res = http.request.render(
                "onboarding_app.tasks",
                {"tasks": task_list},
            )

            return res
