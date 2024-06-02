{
    "name": "Onboarding Application",
    "description": "Human Resources",
    "summary": "Onboarding App",
    "author": "Amnil Tech Team",
    "depends": ["base", "web", "mail"],
    "application": True,
    "data": [
        "data/onboarding_stage.xml",
        "security/ir.model.access.csv",
        "wizard/send_to_approval_view.xml",
        "wizard/approval_view.xml",
        "wizard/ongoing_view.xml",
        "wizard/email_invited_view.xml",
        "wizard/confirm_view.xml",
        "views/onboarding_menu.xml",
        "views/onboarding_view.xml",
    ],
}
