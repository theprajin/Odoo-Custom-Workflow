{
    "name": "Accounting Application",
    "description": "Human Resources",
    "summary": "Accounting App",
    "author": "Amnil Tech Team",
    "category": "Accounting",
    "depends": [
        "base",
        "account",
        "l10n_generic_coa",
    ],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/account_move_views.xml",
        "wizard/file_upload_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "accounting_app/static/src/components/**/*",
        ],
    },
}
