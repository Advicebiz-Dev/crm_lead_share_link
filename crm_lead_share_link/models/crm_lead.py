from odoo import _, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def action_share_internal_link(self):
        self.ensure_one()
        return {
            "name": _("Compartilhar Lead"),
            "type": "ir.actions.act_window",
            "res_model": "crm.lead.share.link.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_lead_id": self.id,
                "active_id": self.id,
                "active_model": self._name,
                "dialog_size": "medium",
            },
        }
