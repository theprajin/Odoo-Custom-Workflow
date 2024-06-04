{
    "name": "Onboarding Application",
    "description": "Human Resources",
    "summary": "Onboarding App",
    "author": "Amnil Tech Team",
    "depends": ["base", "web", "mail"],
    "application": True,
    "data": [
        "data/onboarding_stage.xml",
        "data/department.xml",
        "data/job_position.xml",
        "data/task_type.xml",
        "data/task.xml",
        "data/tag.xml",
        "data/send_email_invitation_template.xml",
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
