{
    "name": "Onboarding Application",
    "description": "Human Resources",
    "summary": "Onboarding App",
    "author": "Amnil Tech Team",
    "depends": [
        "base",
        "web",
    ],
    "application": True,
    "data": [
        "data/onboarding_stage.xml",
        "security/ir.model.access.csv",
        "wizard/send_to_approval_view.xml",
        "views/onboarding_menu.xml",
        "views/onboarding_view.xml",
    ],
}
