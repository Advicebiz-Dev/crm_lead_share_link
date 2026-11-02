{
    "name": "CRM Lead Share Link",
    "summary": "Adds a task-style Share dialog to CRM leads and opportunities",
    "version": "19.0.1.1.0",
    "category": "Sales/CRM",
    "author": "Cátia Silva Advicebiz",
    "license": "LGPL-3",
    "depends": ["crm", "mail", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_lead_share_views.xml",
        "wizard/crm_lead_share_link_wizard_views.xml"
    ],
    "installable": True,
    "application": False
}
